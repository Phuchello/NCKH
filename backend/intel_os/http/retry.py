"""HTTP Retry Policy and Retry-After Header Parsing.

Provides exponential backoff with jitter, Retry-After header parsing (both seconds and HTTP dates),
and selective status code/exception filtering.
"""

from email.utils import parsedate_to_datetime
import random
import time
from typing import Optional, Set

import httpx

# Status codes considered transient and safe for retry
RETRYABLE_STATUS_CODES: Set[int] = {
    429,  # Too Many Requests (Rate Limited)
    502,  # Bad Gateway
    503,  # Service Unavailable
    504,  # Gateway Timeout
}

# Network exceptions safe for retry
RETRYABLE_EXCEPTIONS = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.NetworkError,
)


def parse_retry_after(header_val: Optional[str], max_cap_seconds: float = 60.0) -> Optional[float]:
    """Parses standard HTTP 'Retry-After' header value into seconds.

    Supports both integer seconds and RFC 2822 HTTP date strings.

    Args:
        header_val: Raw string from response.headers.get("Retry-After")
        max_cap_seconds: Maximum allowed delay cap to prevent deadlocks.
    Returns:
        Delay in seconds, or None if invalid/missing.
    """
    if not header_val or not isinstance(header_val, str):
        return None

    cleaned = header_val.strip()

    # 1. Try parsing as numeric seconds (e.g. "120" or "5.5")
    try:
        seconds = float(cleaned)
        if seconds >= 0:
            return min(seconds, max_cap_seconds)
    except ValueError:
        pass

    # 2. Try parsing as HTTP Date string (e.g. "Wed, 21 Oct 2026 07:28:00 GMT")
    try:
        target_dt = parsedate_to_datetime(cleaned)
        now_ts = time.time()
        delay = target_dt.timestamp() - now_ts
        if delay > 0:
            return min(delay, max_cap_seconds)
        return 0.0
    except Exception:
        pass

    return None


def compute_backoff_delay(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    jitter: float = 0.5,
) -> float:
    """Computes exponential backoff delay with random jitter.

    Formula: min(max_delay, base_delay * (2 ** attempt)) + uniform(0, jitter)
    """
    exponential = base_delay * (2 ** attempt)
    capped = min(exponential, max_delay)
    random_jitter = random.uniform(0, jitter)
    return capped + random_jitter
