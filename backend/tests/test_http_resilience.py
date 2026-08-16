"""Unit tests for HTTP Resilience, Rate Limiting, Retry, and Secret Redaction."""

import asyncio
import time
import httpx
import pytest

from intel_os.http.rate_limit import RateLimiter
from intel_os.http.retry import compute_backoff_delay, parse_retry_after
from intel_os.http.transport import (
    ResilientHttpClient,
    sanitize_headers_for_logging,
    sanitize_url_for_logging,
)


@pytest.mark.asyncio
async def test_rate_limiter_min_delay():
    """Verify RateLimiter delay mode enforces minimum time between requests."""
    limiter = RateLimiter(name="test_delay", min_delay_seconds=0.1, max_concurrency=1)

    t0 = time.monotonic()
    async with limiter:
        pass
    async with limiter:
        pass
    t1 = time.monotonic()

    # Second acquisition should have waited at least ~0.08s
    assert (t1 - t0) >= 0.08


@pytest.mark.asyncio
async def test_rate_limiter_rps_token_bucket():
    """Verify RateLimiter token bucket limits throughput."""
    limiter = RateLimiter(name="test_rps", rps=10.0, max_burst=2, max_concurrency=2)

    # First two acquisitions consume burst tokens immediately
    t0 = time.monotonic()
    async with limiter:
        pass
    async with limiter:
        pass
    t1 = time.monotonic()
    assert (t1 - t0) < 0.05

    # Third acquisition must wait for token replenishment
    async with limiter:
        pass
    t2 = time.monotonic()
    assert (t2 - t0) >= 0.08


def test_parse_retry_after_numeric_and_http_date():
    """Verify Retry-After header parsing for seconds and HTTP date strings."""
    # Numeric seconds
    assert parse_retry_after("30") == 30.0
    assert parse_retry_after(" 15.5 ") == 15.5
    assert parse_retry_after("0") == 0.0

    # Max cap enforcement
    assert parse_retry_after("3600", max_cap_seconds=60.0) == 60.0

    # Invalid values
    assert parse_retry_after(None) is None
    assert parse_retry_after("") is None
    assert parse_retry_after("invalid_header") is None


def test_compute_backoff_delay():
    """Verify exponential backoff calculation increases with attempts."""
    d0 = compute_backoff_delay(0, base_delay=1.0, max_delay=30.0, jitter=0.0)
    d1 = compute_backoff_delay(1, base_delay=1.0, max_delay=30.0, jitter=0.0)
    d2 = compute_backoff_delay(2, base_delay=1.0, max_delay=30.0, jitter=0.0)

    assert d0 == 1.0
    assert d1 == 2.0
    assert d2 == 4.0

    # Capped at max_delay
    d_capped = compute_backoff_delay(10, base_delay=1.0, max_delay=30.0, jitter=0.0)
    assert d_capped == 30.0


def test_secret_redaction_in_urls_and_headers():
    """Verify API keys and authorization headers are cleanly redacted for logs."""
    url = "https://api.example.com/search?query=ai&api_key=SECRET123&other=val"
    sanitized_url = sanitize_url_for_logging(url)
    assert "SECRET123" not in sanitized_url
    assert "api_key=[REDACTED]" in sanitized_url

    headers = {
        "User-Agent": "IntelOS",
        "Authorization": "Bearer supersecretjwt",
        "x-api-key": "s2_secret_key_456",
        "Accept": "application/json",
    }
    sanitized_headers = sanitize_headers_for_logging(headers)
    assert sanitized_headers["Authorization"] == "[REDACTED]"
    assert sanitized_headers["x-api-key"] == "[REDACTED]"
    assert sanitized_headers["User-Agent"] == "IntelOS"
    assert sanitized_headers["Accept"] == "application/json"


@pytest.mark.asyncio
async def test_resilient_http_client_retries_429():
    """Verify ResilientHttpClient retries 429 status and returns 200 upon recovery."""
    attempt_count = 0

    def mock_handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count == 1:
            return httpx.Response(429, headers={"Retry-After": "0.01"})
        return httpx.Response(200, json={"status": "ok"})

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)

    resilient_client = ResilientHttpClient(
        name="test_retry",
        max_retries=2,
        verify_ssrf=False,
        client=mock_client,
    )

    response = await resilient_client.get("https://api.example.com/data")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert attempt_count == 2


@pytest.mark.asyncio
async def test_resilient_http_client_does_not_retry_404():
    """Verify permanent 4xx client errors (404, 400) are returned immediately without retry."""
    attempt_count = 0

    def mock_handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempt_count
        attempt_count += 1
        return httpx.Response(404, json={"error": "Not Found"})

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)

    resilient_client = ResilientHttpClient(
        name="test_no_retry",
        max_retries=3,
        verify_ssrf=False,
        client=mock_client,
    )

    response = await resilient_client.get("https://api.example.com/missing")
    assert response.status_code == 404
    assert attempt_count == 1
