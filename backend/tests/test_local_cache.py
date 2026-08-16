"""Tests for LocalCacheManager Bounded Storage and Path Security Guardrails."""

from pathlib import Path
import time
import pytest

from intel_os.storage.local_cache import CacheSecurityError, LocalCacheManager


def test_cache_put_get_delete(cache_manager: LocalCacheManager):
    """Validates basic cache write, read, and delete operations."""
    test_data = b"Hello, Intel OS Local Cache!"
    rel_path = "papers/arxiv_2403_001.pdf"

    saved_path = cache_manager.put(rel_path, test_data)
    assert saved_path.exists()
    assert saved_path.read_bytes() == test_data

    # Read back
    retrieved = cache_manager.get(rel_path)
    assert retrieved == test_data

    # Check usage
    usage = cache_manager.get_usage()
    assert usage.file_count == 1
    assert usage.current_bytes == len(test_data)

    # Delete
    deleted = cache_manager.delete(rel_path)
    assert deleted is True
    assert cache_manager.get(rel_path) is None


def test_cache_security_path_traversal(cache_manager: LocalCacheManager):
    """CRITICAL SECURITY: Path traversal attempts must be blocked with CacheSecurityError."""
    # Attempting to write outside cache root
    with pytest.raises(CacheSecurityError):
        cache_manager.put("../../escaped_file.txt", b"malicious payload")

    # Attempting to get outside cache root
    with pytest.raises(CacheSecurityError):
        cache_manager.get("../../../etc/passwd")

    # Attempting to delete outside cache root
    with pytest.raises(CacheSecurityError):
        cache_manager.delete("../outside.txt")


def test_cache_lru_pruning(tmp_path: Path):
    """Validates deterministic LRU eviction when budget is breached."""
    # Create small cache manager with ~300 bytes max budget
    mgr = LocalCacheManager(cache_dir=tmp_path / "lru_test", max_cache_gb=0.0000003)  # ~322 bytes
    mgr.max_bytes = 300

    # Write 3 files (100 bytes each)
    f1_data = b"A" * 100
    f2_data = b"B" * 100
    f3_data = b"C" * 100

    mgr.put("file1.bin", f1_data)
    time.sleep(0.05)
    mgr.put("file2.bin", f2_data)
    time.sleep(0.05)
    mgr.put("file3.bin", f3_data)

    usage = mgr.get_usage()
    assert usage.current_bytes == 300
    assert usage.file_count == 3

    # Access file1 to update its access time, making file2 the oldest
    _ = mgr.get("file1.bin")

    # Write a 4th file to trigger over-budget eviction
    f4_data = b"D" * 100
    mgr.put("file4.bin", f4_data)

    # After automated pruning, total bytes should be <= 300 * 0.8 = 240 bytes
    new_usage = mgr.get_usage()
    assert new_usage.current_bytes <= 240


def test_cache_clear(cache_manager: LocalCacheManager):
    """Validates full cache clearing while preserving root directory."""
    cache_manager.put("dir1/file1.txt", b"data1")
    cache_manager.put("dir2/file2.txt", b"data2")

    assert cache_manager.get_usage().file_count == 2

    removed = cache_manager.clear()
    assert removed == 2
    assert cache_manager.get_usage().file_count == 0
    assert cache_manager.cache_dir.exists()
