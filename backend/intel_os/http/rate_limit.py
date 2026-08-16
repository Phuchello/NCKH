"""Rate Limiting Subsystem for External Academic APIs.

Provides token bucket and minimum delay rate limiters to comply with
official provider rate policies (arXiv 3s politeness, Crossref polite pool, OpenAlex, Semantic Scholar).
"""

import asyncio
import time
from typing import Optional


class RateLimiter:
    """Async Rate Limiter supporting requests-per-second or minimum inter-request delay."""

    def __init__(
        self,
        name: str,
        rps: Optional[float] = None,
        min_delay_seconds: Optional[float] = None,
        max_burst: int = 1,
        max_concurrency: int = 5,
    ) -> None:
        """Initializes rate limiter.

        Args:
            name: Provider or limiter name (for logging).
            rps: Allowed requests per second (token bucket mode).
            min_delay_seconds: Minimum delay between requests (delay mode, e.g. arXiv 3.0s).
            max_burst: Maximum token capacity for burst handling in RPS mode.
            max_concurrency: Maximum concurrent active in-flight requests.
        """
        self.name = name
        self.rps = rps
        self.min_delay_seconds = min_delay_seconds
        self.max_burst = max(1, max_burst)
        self.max_concurrency = max_concurrency

        self._lock = asyncio.Lock()
        self._semaphore = asyncio.Semaphore(max_concurrency)

        # State for token bucket (RPS mode)
        self._tokens: float = float(self.max_burst)
        self._last_token_update: float = time.monotonic()

        # State for min delay mode
        self._last_request_time: float = 0.0

    async def acquire(self) -> None:
        """Waits until a request is permitted under the rate limit policy."""
        await self._semaphore.acquire()
        try:
            async with self._lock:
                now = time.monotonic()

                # 1. Enforce minimum delay mode (e.g. arXiv 3.0s)
                if self.min_delay_seconds is not None and self.min_delay_seconds > 0:
                    elapsed = now - self._last_request_time
                    delay = self.min_delay_seconds - elapsed
                    if delay > 0:
                        await asyncio.sleep(delay)
                    self._last_request_time = time.monotonic()
                    return

                # 2. Enforce RPS token bucket mode
                if self.rps is not None and self.rps > 0:
                    elapsed = now - self._last_token_update
                    self._last_token_update = now
                    # Add newly accumulated tokens
                    self._tokens = min(self.max_burst, self._tokens + (elapsed * self.rps))

                    if self._tokens < 1.0:
                        wait_seconds = (1.0 - self._tokens) / self.rps
                        await asyncio.sleep(wait_seconds)
                        self._tokens = 0.0
                        self._last_token_update = time.monotonic()
                    else:
                        self._tokens -= 1.0
        except BaseException:
            self._semaphore.release()
            raise

    def release(self) -> None:
        """Releases the concurrency slot after request finishes."""
        self._semaphore.release()

    async def __aenter__(self) -> "RateLimiter":
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()
