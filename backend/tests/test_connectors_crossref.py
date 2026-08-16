"""Unit tests for Crossref Connector."""

import httpx
import pytest

from intel_os.connectors.crossref import CrossrefConnector, clean_jats_abstract
from intel_os.http.transport import ResilientHttpClient

SAMPLE_CROSSREF_JSON = {
    "status": "ok",
    "message-type": "work-list",
    "message": {
        "items": [
            {
                "DOI": "10.1145/3372278.3390678",
                "title": ["A Graph-Based Framework for Research Gap Detection"],
                "author": [
                    {"given": "Jane", "family": "Doe"},
                    {"given": "John", "family": "Smith"},
                ],
                "abstract": "<jats:p>We propose a novel <jats:italic>framework</jats:italic> for detecting research gaps.</jats:p>",
                "container-title": ["ACM Transactions on Information Systems"],
                "published-print": {"date-parts": [[2020, 6, 15]]},
                "URL": "http://dx.doi.org/10.1145/3372278.3390678",
                "type": "journal-article",
                "publisher": "Association for Computing Machinery (ACM)",
                "is-referenced-by-count": 42,
            }
        ]
    },
}


def test_clean_jats_abstract():
    """Verify stripping of JATS XML tags in Crossref abstracts."""
    raw = "<jats:p>This is <jats:bold>important</jats:bold> research with <jats:italic>p &lt; 0.05</jats:italic>.</jats:p>"
    cleaned = clean_jats_abstract(raw)
    assert cleaned == "This is important research with p &lt; 0.05."


@pytest.mark.asyncio
async def test_crossref_connector_search_and_parse():
    """Verify parsing of Crossref JSON payload into NormalizedDiscoveryRecord."""
    def mock_handler(request: httpx.Request) -> httpx.Response:
        assert "mailto=" in str(request.url) or "mailto" in request.headers
        return httpx.Response(200, json=SAMPLE_CROSSREF_JSON)

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)
    resilient_client = ResilientHttpClient(name="mock_crossref", verify_ssrf=False, client=mock_client)

    connector = CrossrefConnector(http_client=resilient_client)
    records = await connector.search(query="research gap detection", limit=1)

    assert len(records) == 1
    rec = records[0]

    assert rec.provider == "crossref"
    assert rec.doi == "10.1145/3372278.3390678"
    assert rec.title == "A Graph-Based Framework for Research Gap Detection"
    assert rec.authors == ["Jane Doe", "John Smith"]
    assert rec.venue == "ACM Transactions on Information Systems"
    assert rec.publication_year == 2020
    assert rec.canonical_url == "https://doi.org/10.1145/3372278.3390678"
    assert rec.abstract == "We propose a novel framework for detecting research gaps."
    assert rec.provider_metadata["is_referenced_by_count"] == 42


@pytest.mark.asyncio
async def test_crossref_connector_fetch_by_id():
    """Verify single paper fetch by DOI."""
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"status": "ok", "message": SAMPLE_CROSSREF_JSON["message"]["items"][0]})

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)
    resilient_client = ResilientHttpClient(name="mock_crossref", verify_ssrf=False, client=mock_client)

    connector = CrossrefConnector(http_client=resilient_client)
    rec = await connector.fetch_by_id("10.1145/3372278.3390678")

    assert rec is not None
    assert rec.doi == "10.1145/3372278.3390678"
