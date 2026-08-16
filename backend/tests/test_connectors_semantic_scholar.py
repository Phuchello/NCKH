"""Unit tests for Semantic Scholar Connector."""

import httpx
import pytest

from intel_os.connectors.semantic_scholar import SemanticScholarConnector
from intel_os.http.transport import ResilientHttpClient

SAMPLE_S2_JSON = {
    "total": 1,
    "offset": 0,
    "data": [
        {
            "paperId": "649def34f8be52c8b66281af98ae772c99cf93e5",
            "corpusId": 215789642,
            "title": "A Graph-Based Framework for Research Gap Detection",
            "abstract": "We propose a novel framework for detecting research gaps in scientific literature.",
            "venue": "ACM Trans. Inf. Syst.",
            "year": 2020,
            "publicationDate": "2020-06-15",
            "authors": [
                {"authorId": "12345", "name": "Jane Doe"},
                {"authorId": "67890", "name": "John Smith"},
            ],
            "externalIds": {
                "DOI": "10.1145/3372278.3390678",
                "ArXiv": "2006.12345v1",
                "CorpusId": "215789642",
            },
            "url": "https://www.semanticscholar.org/paper/649def34f8be52c8b66281af98ae772c99cf93e5",
            "openAccessPdf": {
                "url": "https://dl.acm.org/doi/pdf/10.1145/3372278.3390678",
                "status": "GREEN",
            },
            "citationCount": 60,
            "influentialCitationCount": 12,
        }
    ],
}


@pytest.mark.asyncio
async def test_semantic_scholar_connector_search_and_parse():
    """Verify Semantic Scholar search parsing and externalIds mapping."""
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=SAMPLE_S2_JSON)

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)
    resilient_client = ResilientHttpClient(name="mock_s2", verify_ssrf=False, client=mock_client)

    connector = SemanticScholarConnector(http_client=resilient_client)
    records = await connector.search(query="graph gap detection", limit=1)

    assert len(records) == 1
    rec = records[0]

    assert rec.provider == "semantic_scholar"
    assert rec.provider_document_id == "649def34f8be52c8b66281af98ae772c99cf93e5"
    assert rec.doi == "10.1145/3372278.3390678"
    assert rec.arxiv_id == "2006.12345"  # Logical normalized ID
    assert rec.title == "A Graph-Based Framework for Research Gap Detection"
    assert rec.authors == ["Jane Doe", "John Smith"]
    assert rec.venue == "ACM Trans. Inf. Syst."
    assert rec.publication_year == 2020
    assert rec.canonical_url == "https://doi.org/10.1145/3372278.3390678"
    assert rec.external_ids["corpus_id"] == "215789642"
    assert rec.provider_metadata["citationCount"] == 60


@pytest.mark.asyncio
async def test_semantic_scholar_connector_batch_fetch():
    """Verify Semantic Scholar batch endpoint handling."""
    def mock_handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/paper/batch" in str(request.url)
        return httpx.Response(200, json=SAMPLE_S2_JSON["data"])

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)
    resilient_client = ResilientHttpClient(name="mock_s2", verify_ssrf=False, client=mock_client)

    connector = SemanticScholarConnector(http_client=resilient_client)
    records = await connector.batch_fetch(["649def34f8be52c8b66281af98ae772c99cf93e5"])

    assert len(records) == 1
    assert records[0].provider_document_id == "649def34f8be52c8b66281af98ae772c99cf93e5"
