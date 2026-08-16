"""Network Safety and SSRF Mitigation Module.

Provides pre-flight URL validation, hostname IP resolution checks,
and redirect safety controls to protect internal infrastructure from SSRF attacks.
"""

import ipaddress
import socket
from urllib.parse import urljoin, urlparse

# Blocked IP Networks for SSRF Mitigation
BLOCKED_IP_NETWORKS = [
    # IPv4 Private & Reserved Ranges (RFC 1918, RFC 3927, RFC 1122, etc.)
    ipaddress.ip_network("0.0.0.0/8"),          # Current network (only valid as source)
    ipaddress.ip_network("127.0.0.0/8"),        # Loopback
    ipaddress.ip_network("10.0.0.0/8"),         # Private-use (RFC 1918)
    ipaddress.ip_network("172.16.0.0/12"),      # Private-use (RFC 1918)
    ipaddress.ip_network("192.168.0.0/16"),     # Private-use (RFC 1918)
    ipaddress.ip_network("169.254.0.0/16"),     # Link-local (includes AWS/GCP metadata 169.254.169.254)
    ipaddress.ip_network("255.255.255.255/32"), # Broadcast
    # IPv6 Loopback, Link-Local & Unique-Local
    ipaddress.ip_network("::1/128"),            # IPv6 Loopback
    ipaddress.ip_network("::/128"),             # IPv6 Unspecified
    ipaddress.ip_network("fc00::/7"),           # IPv6 Unique Local Address (ULA)
    ipaddress.ip_network("fe80::/10"),          # IPv6 Link-Local
]

ALLOWED_SCHEMES = frozenset({"http", "https"})


class NetworkSafetyError(ValueError):
    """Raised when a URL or resolved network endpoint violates security policies."""


def is_ip_blocked(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """Checks if an IP address belongs to any blocked private/reserved range."""
    return any(ip in network for network in BLOCKED_IP_NETWORKS)


def validate_url_syntax(url: str) -> tuple[str, str, int | None]:
    """Validates URL syntax, scheme, and userinfo constraints.

    Returns:
        tuple of (scheme, hostname, port)
    Raises:
        NetworkSafetyError: If scheme is disallowed, host is missing, or userinfo is present.
    """
    if not url or not isinstance(url, str):
        raise NetworkSafetyError("URL must be a non-empty string.")

    parsed = urlparse(url.strip())

    scheme = parsed.scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        raise NetworkSafetyError(
            f"Disallowed URL scheme '{scheme}'. Only HTTP and HTTPS are permitted."
        )

    # Reject userinfo in URL (e.g. http://user:pass@example.com)
    if parsed.username or parsed.password:
        raise NetworkSafetyError("URLs containing userinfo/credentials are not permitted.")

    hostname = parsed.hostname
    if not hostname:
        raise NetworkSafetyError(f"Invalid URL '{url}': hostname is missing.")

    return scheme, hostname.lower(), parsed.port


def validate_url_safety(url: str, resolve_dns: bool = True) -> str:
    """Performs full pre-flight SSRF validation on a target URL.

    Checks scheme, userinfo, and resolves the target hostname to ensure
    it does not map to loopback, private RFC 1918, or cloud metadata IP ranges.

    Returns:
        The validated URL string.
    Raises:
        NetworkSafetyError: If the URL or target IP violates security policy.
    """
    scheme, hostname, _ = validate_url_syntax(url)

    # Check if hostname is already an IP address literal
    ip: ipaddress.IPv4Address | ipaddress.IPv6Address | None = None
    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        ip = None

    if ip is not None:
        if is_ip_blocked(ip):
            raise NetworkSafetyError(
                f"Access to IP address '{ip}' is blocked by SSRF defense policy."
            )
        return url

    # Quick literal loopback/metadata check on host strings
    if hostname in ("localhost", "ip6-localhost", "ip6-loopback"):
        raise NetworkSafetyError(f"Access to '{hostname}' is blocked by SSRF defense policy.")

    if not resolve_dns:
        return url

    # Resolve hostname to all associated IPs and verify none are blocked
    try:
        addr_info = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise NetworkSafetyError(f"DNS resolution failed for host '{hostname}': {exc}") from exc

    resolved_ips: list[ipaddress.IPv4Address | ipaddress.IPv6Address] = []
    for item in addr_info:
        sockaddr = item[4]
        ip_str = sockaddr[0]
        try:
            ip = ipaddress.ip_address(ip_str)
            resolved_ips.append(ip)
            if is_ip_blocked(ip):
                raise NetworkSafetyError(
                    f"Host '{hostname}' resolved to blocked IP '{ip}' (SSRF defense)."
                )
        except ValueError:
            continue

    if not resolved_ips:
        raise NetworkSafetyError(f"Host '{hostname}' could not be resolved to any valid IP address.")

    return url


def validate_redirect_url(current_url: str, redirect_location: str) -> str:
    """Resolves and validates a redirect location URL against SSRF policy."""
    target_url = urljoin(current_url, redirect_location)
    return validate_url_safety(target_url, resolve_dns=True)
