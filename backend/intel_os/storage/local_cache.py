"""Intel OS Local Cache Manager.

Enforces bounded local storage quotas with LRU eviction and strict path safety boundaries.
"""

from dataclasses import dataclass
import logging
import os
from pathlib import Path
import time
from typing import List, Optional

from intel_os.core.config import get_settings

logger = logging.getLogger(__name__)


class CacheSecurityError(Exception):
    """Raised when an operation attempts to access or modify paths outside the cache root."""


@dataclass
class CacheUsage:
    """Snapshot of current cache utilization."""

    current_bytes: int
    max_bytes: int
    file_count: int

    @property
    def usage_ratio(self) -> float:
        """Ratio of current usage to maximum budget (0.0 to 1.0+)."""
        if self.max_bytes <= 0:
            return 0.0
        return self.current_bytes / self.max_bytes

    @property
    def is_over_budget(self) -> bool:
        """True if current usage exceeds max budget."""
        return self.current_bytes > self.max_bytes


@dataclass
class PruneResult:
    """Summary of cache pruning operation."""

    files_removed: int
    bytes_reclaimed: int
    remaining_bytes: int


class LocalCacheManager:
    """Manages transient local file buffers with quota enforcement and LRU eviction."""

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        max_cache_gb: Optional[float] = None,
    ) -> None:
        settings = get_settings()
        self.cache_dir = (cache_dir or settings.LOCAL_TEMP_DIR).resolve()
        self.max_bytes = int(
            (max_cache_gb if max_cache_gb is not None else settings.MAX_LOCAL_CACHE_GB)
            * 1024
            * 1024
            * 1024
        )
        self.ensure_cache_dir()

    def ensure_cache_dir(self) -> None:
        """Ensures the cache root directory exists."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_safe_path(self, relative_path: str | Path) -> Path:
        """Resolves a path and verifies it resides strictly inside the cache root.

        Prevents directory traversal attacks (e.g. '../', '/etc/passwd').
        """
        # Resolve target path
        target = (self.cache_dir / relative_path).resolve()

        # Strict containment check
        try:
            target.relative_to(self.cache_dir)
        except ValueError as exc:
            raise CacheSecurityError(
                f"Path traversal detected: '{relative_path}' escapes cache root '{self.cache_dir}'"
            ) from exc

        return target

    def get_usage(self) -> CacheUsage:
        """Calculates total disk usage and file count within the cache directory."""
        total_bytes = 0
        file_count = 0

        if not self.cache_dir.exists():
            return CacheUsage(current_bytes=0, max_bytes=self.max_bytes, file_count=0)

        for root, _, files in os.walk(self.cache_dir):
            for file in files:
                file_path = Path(root) / file
                try:
                    total_bytes += file_path.stat().st_size
                    file_count += 1
                except (OSError, FileNotFoundError):
                    # Gracefully handle transient files / races
                    continue

        return CacheUsage(
            current_bytes=total_bytes,
            max_bytes=self.max_bytes,
            file_count=file_count,
        )

    def put(self, relative_path: str | Path, data: bytes) -> Path:
        """Writes binary data to the cache, creating parent directories safely."""
        target_path = self._resolve_safe_path(relative_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        target_path.write_bytes(data)
        logger.debug("Cached %d bytes to %s", len(data), target_path)

        # Check budget and trigger pruning if over budget
        usage = self.get_usage()
        if usage.is_over_budget:
            logger.warning(
                "Cache exceeded quota (%d / %d bytes). Triggering automated LRU eviction.",
                usage.current_bytes,
                usage.max_bytes,
            )
            self.prune()

        return target_path

    def get(self, relative_path: str | Path) -> Optional[bytes]:
        """Reads data from cache, updating access time for LRU tracking."""
        target_path = self._resolve_safe_path(relative_path)
        if not target_path.is_file():
            return None

        try:
            # Update access time (atime)
            os.utime(target_path, None)
            return target_path.read_bytes()
        except (OSError, FileNotFoundError):
            return None

    def delete(self, relative_path: str | Path) -> bool:
        """Safely deletes a specific file from cache."""
        target_path = self._resolve_safe_path(relative_path)
        try:
            if target_path.is_file():
                target_path.unlink()
                return True
        except (OSError, FileNotFoundError):
            pass
        return False

    def prune(self, target_ratio: float = 0.8) -> PruneResult:
        """Evicts oldest accessed files until cache usage is below target_ratio * max_bytes.

        Args:
            target_ratio: Target budget ratio after cleanup (default 0.8 = 80% of max budget).
        """
        usage = self.get_usage()
        target_bytes = int(self.max_bytes * target_ratio)

        if usage.current_bytes <= target_bytes:
            return PruneResult(
                files_removed=0,
                bytes_reclaimed=0,
                remaining_bytes=usage.current_bytes,
            )

        # Collect all files with access/modification time and size
        file_entries: List[tuple[Path, float, int]] = []
        for root, _, files in os.walk(self.cache_dir):
            for file in files:
                file_path = Path(root) / file
                try:
                    stat = file_path.stat()
                    # Use last access time if available, fallback to mtime
                    atime = getattr(stat, "st_atime", stat.st_mtime)
                    file_entries.append((file_path, atime, stat.st_size))
                except (OSError, FileNotFoundError):
                    continue

        # Sort by access time ascending (oldest first)
        file_entries.sort(key=lambda x: x[1])

        files_removed = 0
        bytes_reclaimed = 0
        current_bytes = usage.current_bytes

        for file_path, _, size in file_entries:
            if current_bytes <= target_bytes:
                break
            try:
                # Double check path containment before deletion
                file_path.resolve().relative_to(self.cache_dir)
                file_path.unlink()
                files_removed += 1
                bytes_reclaimed += size
                current_bytes -= size
            except (OSError, FileNotFoundError, ValueError) as exc:
                logger.warning("Failed to evict cached file %s: %s", file_path, exc)
                continue

        logger.info(
            "Pruned %d files, reclaimed %d bytes. Current usage: %d bytes.",
            files_removed,
            bytes_reclaimed,
            current_bytes,
        )

        return PruneResult(
            files_removed=files_removed,
            bytes_reclaimed=bytes_reclaimed,
            remaining_bytes=current_bytes,
        )

    def clear(self) -> int:
        """Removes all cached files while preserving the root directory."""
        removed_count = 0
        for root, dirs, files in os.walk(self.cache_dir, topdown=False):
            for file in files:
                file_path = Path(root) / file
                try:
                    file_path.unlink()
                    removed_count += 1
                except (OSError, FileNotFoundError):
                    pass
            for d in dirs:
                dir_path = Path(root) / d
                try:
                    dir_path.rmdir()
                except (OSError, FileNotFoundError):
                    pass
        return removed_count
