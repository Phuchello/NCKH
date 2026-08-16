"""Tests for URL Normalization and Canonical Identity Rules."""

import pytest
from intel_os.core.url import normalize_url


def test_url_normalization_scheme_and_host_casing():
    """Validates lowercase conversion for scheme and hostname."""
    url1 = "HTTPS://ARXIV.ORG/abs/2403.00001"
    url2 = "https://arxiv.org/abs/2403.00001"
    assert normalize_url(url1) == "https://arxiv.org/abs/2403.00001"
    assert normalize_url(url1) == normalize_url(url2)


def test_url_normalization_default_ports():
    """Validates removal of standard default ports."""
    assert normalize_url("http://example.com:80/paper") == "http://example.com/paper"
    assert normalize_url("https://example.com:443/paper") == "https://example.com/paper"
    assert normalize_url("https://example.com:8443/paper") == "https://example.com:8443/paper"


def test_url_normalization_fragments():
    """Validates stripping of URL fragments."""
    url = "https://arxiv.org/abs/2403.00001#section.2"
    assert normalize_url(url) == "https://arxiv.org/abs/2403.00001"


def test_url_normalization_trailing_slash():
    """Validates trailing slash stripping for paths."""
    assert normalize_url("https://arxiv.org/abs/2403.00001/") == "https://arxiv.org/abs/2403.00001"
    assert normalize_url("https://arxiv.org/") == "https://arxiv.org/"


def test_url_normalization_tracking_parameters():
    """Validates stripping of analytics/tracking parameters while preserving semantic query params."""
    # Tracking parameters removed
    url_tracked = (
        "https://arxiv.org/abs/2403.00001?utm_source=twitter&utm_medium=social&utm_campaign=launch&ref=hacker_news"
    )
    assert normalize_url(url_tracked) == "https://arxiv.org/abs/2403.00001"

    # Semantic parameters preserved and deterministically sorted
    url_semantic = "https://api.crossref.org/works?query=speculative&rows=20&filter=type:journal-article"
    normalized = normalize_url(url_semantic)
    assert "filter=type%3Ajournal-article" in normalized
    assert "query=speculative" in normalized
    assert "rows=20" in normalized

    # Mixed tracking and semantic parameters
    url_mixed = "https://api.crossref.org/works?rows=20&utm_source=feed&query=speculative"
    normalized_mixed = normalize_url(url_mixed)
    assert "utm_source" not in normalized_mixed
    assert "rows=20" in normalized_mixed
    assert "query=speculative" in normalized_mixed


def test_url_normalization_empty_and_whitespace():
    """Validates robust handling of empty and whitespace strings."""
    assert normalize_url("") == ""
    assert normalize_url("   ") == ""
