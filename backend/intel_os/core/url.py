"""URL Normalization and Canonization Utilities.

Provides conservative, deterministic URL normalization for observation identity
and deduplication without destroying semantic query parameters.
"""

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

# Standard tracking and analytics query parameters to safely discard for identity comparison
TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "ref",
    "fbclid",
    "gclid",
    "source",
    "origin",
    "trk",
}


def normalize_url(url: str) -> str:
    """Normalizes a URL deterministically for deduplication identity.

    Rules applied:
    1. Trims leading/trailing whitespace.
    2. Lowercases scheme and hostname.
    3. Removes default scheme ports (:80 for http, :443 for https).
    4. Strips URL fragments (#...).
    5. Strips trailing slash on paths longer than '/'.
    6. Strips known non-semantic tracking parameters (utm_*, ref, etc.).
    7. Sorts remaining semantic query parameters deterministically.
    """
    if not url or not url.strip():
        return ""

    raw_url = url.strip()
    parsed = urlparse(raw_url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Strip default ports
    if scheme == "http" and netloc.endswith(":80"):
        netloc = netloc[:-3]
    elif scheme == "https" and netloc.endswith(":443"):
        netloc = netloc[:-4]

    # Normalize path: strip trailing slash if length > 1
    path = parsed.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")

    # Filter and sort query parameters
    query_params = []
    if parsed.query:
        for k, v in parse_qsl(parsed.query, keep_blank_values=True):
            if k.lower() not in TRACKING_PARAMS:
                query_params.append((k, v))
        query_params.sort(key=lambda x: (x[0], x[1]))

    normalized_query = urlencode(query_params) if query_params else ""

    # Reconstruct URL without fragment
    return urlunparse((scheme, netloc, path, parsed.params, normalized_query, ""))
