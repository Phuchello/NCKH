"""Resilient Async HTTP Client for Academic APIs.

Wraps httpx.AsyncClient with rate limiting, exponential backoff, Retry-After handling,
SSRF pre-flight network safety, and sensitive header redaction.
"""

import asyncio
import re
from typing import Any, Mapping, Optional

import httpx

from intel_os.core.config import get_settings
from intel_os.core.logging import get_logger
from intel_os.http.network_safety import NetworkSafetyError, validate_redirect_url, validate_url_safety
from intel_os.http.rate_limit import RateLimiter
from intel_os.http.retry import RETRYABLE_EXCEPTIONS, RETRYABLE_STATUS_CODES, compute_backoff_delay, parse_retry_after

logger = get_logger(__name__)

# Patterns for sensitive values to redact in logs
SENSITIVE_HEADER_KEYS = {"authorization", "x-api-key", "api-key", "token", "secret"}
SENSITIVE_QUERY_PARAMS = re.compile(r"(api_key|apiKey|token|secret|key)=([^&]+)", re.IGNORECASE)


def sanitize_url_for_logging(url: str) -> str:
    """Redacts sensitive query parameters from URL strings for logging."""
    return SENSITIVE_QUERY_PARAMS.sub(r"\1=[REDACTED]", url)


def sanitize_headers_for_logging(headers: Mapping[str, Any]) -> dict[str, str]:
    """Redacts sensitive authorization and API key headers for safe logging."""
    sanitized = {}
    for k, v in headers.items():
        if k.lower() in SENSITIVE_HEADER_KEYS:
            sanitized[k] = "[REDACTED]"
        else:
            sanitized[k] = str(v)
    return sanitized


class ResilientHttpClient:
    """Resilient asynchronous HTTP client tailored for scholarly API interactions."""

    def __init__(
        self,
        name: str = "default",
        rate_limiter: Optional[RateLimiter] = None,
        max_retries: Optional[int] = None,
        max_redirects: Optional[int] = None,
        verify_ssrf: bool = True,
        headers: Optional[dict[str, str]] = None,
        timeout: Optional[httpx.Timeout] = None,
        client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        """Initializes resilient HTTP client.

        Args:
            name: Provider or client identifier.
            rate_limiter: Optional rate limiter instance.
            max_retries: Max retry attempts on retryable errors.
            max_redirects: Maximum allowed redirect hops.
            verify_ssrf: If True, performs pre-flight SSRF IP validation.
            headers: Default request headers.
            timeout: httpx.Timeout object or None for default settings.
            client: Optional injected httpx.AsyncClient (for testing/mocking).
        """
        settings = get_settings()
        self.name = name
        self.rate_limiter = rate_limiter
        self.max_retries = max_retries if max_retries is not None else settings.HTTP_MAX_RETRIES
        self.max_redirects = max_redirects if max_redirects is not None else settings.HTTP_MAX_REDIRECTS
        self.verify_ssrf = verify_ssrf

        default_headers = {
            "User-Agent": settings.INGEST_USER_AGENT,
            "Accept-Encoding": "gzip, deflate",
        }
        if headers:
            default_headers.update(headers)

        default_timeout = timeout or httpx.Timeout(
            connect=settings.HTTP_CONNECT_TIMEOUT_SECONDS,
            read=settings.HTTP_READ_TIMEOUT_SECONDS,
            write=settings.HTTP_CONNECT_TIMEOUT_SECONDS,
            pool=settings.HTTP_CONNECT_TIMEOUT_SECONDS,
        )

        self._client = client or httpx.AsyncClient(
            headers=default_headers,
            timeout=default_timeout,
            follow_redirects=False,  # Redirects handled manually for SSRF inspection
        )
        self._owns_client = client is None

    async def get(
        self,
        url: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> httpx.Response:
        """Performs a resilient GET request."""
        return await self.request("GET", url, params=params, headers=headers)

    async def post(
        self,
        url: str,
        *,
        json: Optional[Any] = None,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> httpx.Response:
        """Performs a resilient POST request."""
        return await self.request("POST", url, json=json, params=params, headers=headers)

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> httpx.Response:
        """Executes HTTP request with rate limiting, SSRF checks, manual redirect validation, and retries."""
        current_url = url
        redirect_count = 0

        while True:
            # 1. Pre-flight SSRF Validation
            if self.verify_ssrf:
                validate_url_safety(current_url)

            response = await self._execute_with_retry(
                method=method,
                url=current_url,
                params=params if redirect_count == 0 else None,
                json=json if redirect_count == 0 else None,
                data=data if redirect_count == 0 else None,
                headers=headers,
            )

            # 2. Handle HTTP Redirects safely
            if response.is_redirect:
                redirect_count += 1
                if redirect_count > self.max_redirects:
                    raise NetworkSafetyError(
                        f"Exceeded maximum allowed redirects ({self.max_redirects}) for {sanitize_url_for_logging(url)}"
                    )

                location = response.headers.get("Location")
                if not location:
                    return response

                # Validate redirect target against SSRF blocklists
                current_url = validate_redirect_url(str(response.url), location)
                logger.info(
                    f"Following safe redirect ({redirect_count}/{self.max_redirects}) to: {sanitize_url_for_logging(current_url)}"
                )
                # Method switches to GET on 301/302/303 standard redirects
                if response.status_code in (301, 302, 303):
                    method = "GET"
                continue

            return response

    async def _execute_with_retry(
        self,
        method: str,
        url: str,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> httpx.Response:
        """Performs request under rate limiting with exponential backoff on retryable failures."""
        attempt = 0
        last_exception: Optional[Exception] = None

        while attempt <= self.max_retries:
            # Rate limiter acquisition
            if self.rate_limiter:
                await self.rate_limiter.acquire()

            try:
                safe_log_url = sanitize_url_for_logging(url)
                logger.debug(f"HTTP {method} {safe_log_url} (attempt {attempt + 1}/{self.max_retries + 1})")

                response = await self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    data=data,
                    headers=headers,
                )

                # If status code is retryable (429, 502, 503, 504), compute delay and retry
                if response.status_code in RETRYABLE_STATUS_CODES and attempt < self.max_retries:
                    retry_after = parse_retry_after(response.headers.get("Retry-After"))
                    backoff = compute_backoff_delay(attempt)
                    delay = retry_after if retry_after is not None else backoff

                    logger.warning(
                        f"HTTP {response.status_code} for {safe_log_url}. Retrying in {delay:.2f}s "
                        f"(attempt {attempt + 1}/{self.max_retries})"
                    )
                    await asyncio.sleep(delay)
                    attempt += 1
                    continue

                return response

            except RETRYABLE_EXCEPTIONS as exc:
                last_exception = exc
                if attempt < self.max_retries:
                    backoff = compute_backoff_delay(attempt)
                    logger.warning(
                        f"Network error ({type(exc).__name__}) for {sanitize_url_for_logging(url)}. "
                        f"Retrying in {backoff:.2f}s (attempt {attempt + 1}/{self.max_retries})"
                    )
                    await asyncio.sleep(backoff)
                    attempt += 1
                    continue
                raise
            finally:
                if self.rate_limiter:
                    self.rate_limiter.release()

        if last_exception:
            raise last_exception
        raise httpx.HTTPError(f"Failed after {self.max_retries} attempts: {sanitize_url_for_logging(url)}")

    async def close(self) -> None:
        """Closes the underlying HTTP client session."""
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> "ResilientHttpClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
