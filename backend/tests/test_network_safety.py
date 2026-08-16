"""Unit tests for Network Safety and SSRF Mitigation."""

import ipaddress
import pytest

from intel_os.http.network_safety import (
    NetworkSafetyError,
    is_ip_blocked,
    validate_redirect_url,
    validate_url_safety,
    validate_url_syntax,
)


def test_is_ip_blocked_loopback_and_private():
    """Verify loopback, RFC 1918, link-local and cloud metadata IPs are blocked."""
    # Loopback
    assert is_ip_blocked(ipaddress.ip_address("127.0.0.1")) is True
    assert is_ip_blocked(ipaddress.ip_address("127.0.1.1")) is True
    assert is_ip_blocked(ipaddress.ip_address("::1")) is True

    # RFC 1918 Private
    assert is_ip_blocked(ipaddress.ip_address("10.0.0.1")) is True
    assert is_ip_blocked(ipaddress.ip_address("172.16.0.1")) is True
    assert is_ip_blocked(ipaddress.ip_address("172.31.255.255")) is True
    assert is_ip_blocked(ipaddress.ip_address("192.168.1.1")) is True
    assert is_ip_blocked(ipaddress.ip_address("fc00::1")) is True

    # AWS/GCP Metadata & Link-Local
    assert is_ip_blocked(ipaddress.ip_address("169.254.169.254")) is True
    assert is_ip_blocked(ipaddress.ip_address("fe80::1")) is True

    # Public routable IPs should NOT be blocked
    assert is_ip_blocked(ipaddress.ip_address("8.8.8.8")) is False
    assert is_ip_blocked(ipaddress.ip_address("1.1.1.1")) is False
    assert is_ip_blocked(ipaddress.ip_address("93.184.216.34")) is False


def test_validate_url_syntax_valid():
    """Verify standard HTTP/HTTPS URLs pass syntax check."""
    scheme, host, port = validate_url_syntax("https://api.crossref.org/works")
    assert scheme == "https"
    assert host == "api.crossref.org"
    assert port is None

    scheme, host, port = validate_url_syntax("http://export.arxiv.org:8080/api/query")
    assert scheme == "http"
    assert host == "export.arxiv.org"
    assert port == 8080


def test_validate_url_syntax_disallowed_schemes():
    """Verify non-HTTP schemes are rejected."""
    disallowed = [
        "ftp://ftp.example.com/file.txt",
        "file:///etc/passwd",
        "gopher://gopher.example.com",
        "ws://example.com/socket",
        "javascript:alert(1)",
    ]
    for url in disallowed:
        with pytest.raises(NetworkSafetyError, match="Disallowed URL scheme"):
            validate_url_syntax(url)


def test_validate_url_syntax_userinfo_rejection():
    """Verify URLs with embedded credentials/userinfo are rejected."""
    with pytest.raises(NetworkSafetyError, match="userinfo/credentials"):
        validate_url_syntax("https://admin:secret@api.example.com/data")


def test_validate_url_safety_blocks_literal_ips():
    """Verify safety validator blocks raw IP URLs matching private/loopback/metadata."""
    blocked_urls = [
        "http://127.0.0.1:8000/api",
        "http://10.0.0.5/secret",
        "http://192.168.1.100/admin",
        "http://169.254.169.254/latest/meta-data/",
        "http://localhost:8080/test",
    ]
    for url in blocked_urls:
        with pytest.raises(NetworkSafetyError):
            validate_url_safety(url, resolve_dns=False)


def test_validate_redirect_url_safe_and_unsafe():
    """Verify redirect URL validation resolves and checks targets."""
    # Safe relative redirect
    safe_target = validate_redirect_url("https://api.crossref.org/works", "/works/10.1145/123")
    assert safe_target == "https://api.crossref.org/works/10.1145/123"

    # Unsafe redirect to metadata service
    with pytest.raises(NetworkSafetyError):
        validate_redirect_url("https://api.crossref.org/works", "http://169.254.169.254/secret")
