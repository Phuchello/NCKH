"""Unit tests for OpenAlex Connector."""

import httpx
import pytest

from intel_os.connectors.openalex import OpenAlexConnector, reconstruct_inverted_abstract
from intel_os.http.transport import ResilientHttpClient

SAMPLE_OPENALEX_JSON = {
    "meta": {"count": 1, "page": 1, "per_page": 1},
    "results": [
        {
            "id": "https://openalex.org/W2741809807",
            "doi": "https://doi.org/10.1145/3372278.3390678",
            "title": "A Graph-Based Framework for Research Gap Detection",
            "display_name": "A Graph-Based Framework for Research Gap Detection",
            "publication_year": 2020,
            "publication_date": "2020-06-15",
            "authorships": [
                {"author": {"id": "https://openalex.org/A123", "display_name": "Jane Doe"}},
                {"author": {"id": "https://openalex.org/A456", "display_name": "John Smith"}},
            ],
            "abstract_inverted_index": {
                "We": [0],
                "propose": [1],
                "a": [2],
                "novel": [3],
                "graph-based": [4],
                "framework": [5],
                "for": [6],
                "gap": [7],
                "detection.": [8],
            },
            "primary_location": {
                "source": {"display_name": "ACM Transactions on Information Systems"}
            },
            "cited_by_count": 55,
            "concepts": [
                {"display_name": "Information retrieval", "score": 0.85},
                {"display_name": "Knowledge graph", "score": 0.78},
            ],
            "open_access": {
                "is_oa": True,
                "oa_url": "https://dl.acm.org/doi/pdf/10.1145/3372278.3390678",
            },
            "ids": {"mag": 123456789, "openalex": "https://openalex.org/W2741809807"},
        }
    ],
}


def test_reconstruct_inverted_abstract():
    """Verify reconstruct_inverted_abstract reconstructs correct ordered string."""
    inverted = {
        "Deep": [0],
        "learning": [1],
        "enables": [2],
        "effective": [3],
        "discovery.": [4],
    }
    result = reconstruct_inverted_abstract(inverted)
    assert result == "Deep learning enables effective discovery."

    # None and empty checks
    assert reconstruct_inverted_abstract(None) is None
    assert reconstruct_inverted_abstract({}) is None


@pytest.mark.asyncio
async def test_openalex_connector_search_and_parse():
    """Verify OpenAlex search results parsing."""
    def mock_handler(request: httpx.Request) -> httpx.Response:
        assert "mailto=" in str(request.url)
        return httpx.Response(200, json=SAMPLE_OPENALEX_JSON)

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)
    resilient_client = ResilientHttpClient(name="mock_openalex", verify_ssrf=False, client=mock_client)

    connector = OpenAlexConnector(http_client=resilient_client)
    records = await connector.search(query="graph based gap detection", limit=1)

    assert len(records) == 1
    rec = records[0]

    assert rec.provider == "openalex"
    assert rec.provider_document_id == "W2741809807"
    assert rec.doi == "10.1145/3372278.3390678"
    assert rec.title == "A Graph-Based Framework for Research Gap Detection"
    assert rec.authors == ["Jane Doe", "John Smith"]
    assert rec.venue == "ACM Transactions on Information Systems"
    assert rec.publication_year == 2020
    assert rec.abstract == "We propose a novel graph-based framework for gap detection."
    assert rec.external_ids["openalex"] == "W2741809807"
    assert rec.external_ids["mag"] == "123456789"
    assert rec.provider_metadata["cited_by_count"] == 55
    assert "Information retrieval" in rec.provider_metadata["concepts"]


@pytest.mark.asyncio
async def test_openalex_connector_fetch_by_id():
    """Verify single work fetch by OpenAlex ID."""
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=SAMPLE_OPENALEX_JSON["results"][0])

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)
    resilient_client = ResilientHttpClient(name="mock_openalex", verify_ssrf=False, client=mock_client)

    connector = OpenAlexConnector(http_client=resilient_client)
    rec = await connector.fetch_by_id("W2741809807")

    assert rec is not None
    assert rec.provider_document_id == "W2741809807"
    assert rec.doi == "10.1145/3372278.3390678"
