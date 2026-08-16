"""Unit tests for arXiv Connector."""

import httpx
import pytest

from intel_os.connectors.arxiv import ArxivConnector
from intel_os.http.transport import ResilientHttpClient

SAMPLE_ARXIV_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <link href="http://arxiv.org/api/query?search_query=all:electron" rel="self" type="application/atom+xml"/>
  <title type="html">ArXiv Query: search_query=all:electron</title>
  <id>http://arxiv.org/api/123</id>
  <updated>2026-08-16T00:00:00-04:00</updated>
  <entry>
    <id>http://arxiv.org/abs/2301.12345v2</id>
    <updated>2023-02-01T12:00:00Z</updated>
    <published>2023-01-28T10:00:00Z</published>
    <title>
      Deep Residual Learning for Image Recognition
    </title>
    <summary>
      Deeper neural networks are more difficult to train. We present a residual learning framework.
    </summary>
    <author>
      <name>Kaiming He</name>
    </author>
    <author>
      <name>Xiangyu Zhang</name>
    </author>
    <arxiv:doi>10.1109/CVPR.2016.90</arxiv:doi>
    <arxiv:journal_ref>CVPR 2016</arxiv:journal_ref>
  </entry>
</feed>
"""


@pytest.mark.asyncio
async def test_arxiv_connector_search_and_parse():
    """Verify parsing of arXiv Atom XML feed into NormalizedDiscoveryRecord."""
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=SAMPLE_ARXIV_XML)

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)
    resilient_client = ResilientHttpClient(name="mock_arxiv", verify_ssrf=False, client=mock_client)

    connector = ArxivConnector(http_client=resilient_client)
    records = await connector.search(query="deep residual", limit=1)

    assert len(records) == 1
    rec = records[0]

    assert rec.provider == "arxiv"
    assert rec.provider_document_id == "2301.12345"  # Logical ID
    assert rec.arxiv_id == "2301.12345"
    assert rec.title == "Deep Residual Learning for Image Recognition"
    assert rec.authors == ["Kaiming He", "Xiangyu Zhang"]
    assert rec.doi == "10.1109/cvpr.2016.90"
    assert rec.canonical_url == "https://arxiv.org/abs/2301.12345"
    assert rec.observed_url == "http://arxiv.org/abs/2301.12345v2"
    assert rec.publication_year == 2023
    assert rec.external_ids["arxiv_version"] == "v2"
    assert "residual learning framework" in rec.abstract


@pytest.mark.asyncio
async def test_arxiv_connector_fetch_by_id():
    """Verify single paper fetch by ID."""
    def mock_handler(request: httpx.Request) -> httpx.Response:
        assert "id_list=2301.12345" in str(request.url)
        return httpx.Response(200, text=SAMPLE_ARXIV_XML)

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)
    resilient_client = ResilientHttpClient(name="mock_arxiv", verify_ssrf=False, client=mock_client)

    connector = ArxivConnector(http_client=resilient_client)
    rec = await connector.fetch_by_id("2301.12345v2")

    assert rec is not None
    assert rec.arxiv_id == "2301.12345"


@pytest.mark.asyncio
async def test_arxiv_connector_empty_or_malformed_xml():
    """Verify empty or malformed XML feed returns empty list without raising."""
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="<invalid xml")

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)
    resilient_client = ResilientHttpClient(name="mock_arxiv", verify_ssrf=False, client=mock_client)

    connector = ArxivConnector(http_client=resilient_client)
    records = await connector.search(query="test", limit=5)
    assert records == []
