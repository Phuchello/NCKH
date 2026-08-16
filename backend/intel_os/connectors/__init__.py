"""Scholarly Connectors Package and Registry."""

from typing import Optional

from intel_os.connectors.arxiv import ArxivConnector
from intel_os.connectors.base import BaseConnector
from intel_os.connectors.crossref import CrossrefConnector
from intel_os.connectors.openalex import OpenAlexConnector
from intel_os.connectors.semantic_scholar import SemanticScholarConnector
from intel_os.http.transport import ResilientHttpClient

CONNECTOR_REGISTRY = {
    "arxiv": ArxivConnector,
    "crossref": CrossrefConnector,
    "openalex": OpenAlexConnector,
    "semantic_scholar": SemanticScholarConnector,
}


def get_connector(name: str, http_client: Optional[ResilientHttpClient] = None) -> BaseConnector:
    """Factory helper to instantiate a connector by provider name."""
    connector_cls = CONNECTOR_REGISTRY.get(name.lower())
    if not connector_cls:
        raise ValueError(f"Unknown connector provider '{name}'. Available: {list(CONNECTOR_REGISTRY.keys())}")
    return connector_cls(http_client=http_client)


__all__ = [
    "BaseConnector",
    "ArxivConnector",
    "CrossrefConnector",
    "OpenAlexConnector",
    "SemanticScholarConnector",
    "CONNECTOR_REGISTRY",
    "get_connector",
]
