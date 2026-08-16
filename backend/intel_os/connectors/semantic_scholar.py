"""Semantic Scholar Academic Graph API Connector.

Connects to the official Semantic Scholar Graph API v1, handles batch fetching,
extracts multi-repository externalIds, and supports API-key rate limits.
"""

from datetime import date
from typing import Any, List, Optional

from intel_os.connectors.base import BaseConnector
from intel_os.core.config import get_settings
from intel_os.core.logging import get_logger
from intel_os.http.rate_limit import RateLimiter
from intel_os.http.transport import ResilientHttpClient
from intel_os.ingestion.dto import NormalizedDiscoveryRecord
from intel_os.ingestion.identity import normalize_arxiv_id, normalize_doi

logger = get_logger(__name__)

# Standard fields projected for S2 Graph queries
DEFAULT_S2_FIELDS = (
    "paperId,corpusId,title,abstract,authors,year,publicationDate,venue,journal,"
    "externalIds,url,openAccessPdf,citationCount,influentialCitationCount"
)


class SemanticScholarConnector(BaseConnector):
    """Connector for Semantic Scholar Graph API."""

    name: str = "semantic_scholar"
    source_type: str = "graph_index"
    base_url: str = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, http_client: Optional[ResilientHttpClient] = None) -> None:
        settings = get_settings()
        # 1.0 RPS unauthenticated; higher if API key provided
        rps = 10.0 if settings.SEMANTIC_SCHOLAR_API_KEY else settings.SEMANTIC_SCHOLAR_RATE_LIMIT_RPS
        rate_limiter = RateLimiter(
            name="semantic_scholar",
            rps=rps,
            max_burst=2,
            max_concurrency=settings.HTTP_MAX_CONCURRENCY_PER_HOST,
        )

        headers: dict[str, str] = {
            "User-Agent": settings.INGEST_USER_AGENT,
        }
        if settings.SEMANTIC_SCHOLAR_API_KEY:
            headers["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY

        client = http_client or ResilientHttpClient(
            name="semantic_scholar",
            rate_limiter=rate_limiter,
            headers=headers,
        )
        super().__init__(http_client=client)

    async def search(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
        **kwargs: Any,
    ) -> List[NormalizedDiscoveryRecord]:
        """Searches Semantic Scholar papers by relevance query."""
        url = f"{self.base_url}/paper/search"
        params = {
            "query": query,
            "offset": offset,
            "limit": limit,
            "fields": kwargs.get("fields", DEFAULT_S2_FIELDS),
        }
        if "year" in kwargs:
            params["year"] = kwargs["year"]
        if "venue" in kwargs:
            params["venue"] = kwargs["venue"]

        response = await self.http_client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        items = data.get("data", [])
        return self._parse_items(items)

    async def fetch_by_id(self, identifier: str) -> Optional[NormalizedDiscoveryRecord]:
        """Fetches a single paper by Paper ID, DOI (DOI:...), arXiv (ARXIV:...), or CorpusId."""
        url = f"{self.base_url}/paper/{identifier.strip()}"
        params = {"fields": DEFAULT_S2_FIELDS}
        response = await self.http_client.get(url, params=params)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        item = response.json()
        return self._parse_item(item)

    async def batch_fetch(self, identifiers: List[str]) -> List[NormalizedDiscoveryRecord]:
        """Fetches multiple papers in a single bulk batch request."""
        if not identifiers:
            return []
        url = f"{self.base_url}/paper/batch"
        params = {"fields": DEFAULT_S2_FIELDS}
        payload = {"ids": identifiers}
        response = await self.http_client.post(url, params=params, json=payload)
        response.raise_for_status()
        items = response.json()
        return self._parse_items([i for i in items if i is not None])

    def _parse_items(self, items: List[dict]) -> List[NormalizedDiscoveryRecord]:
        """Parses list of Semantic Scholar paper items."""
        records: List[NormalizedDiscoveryRecord] = []
        for item in items:
            try:
                record = self._parse_item(item)
                if record:
                    records.append(record)
            except Exception as exc:
                logger.warning(f"Error parsing Semantic Scholar paper: {exc}", exc_info=True)
                continue
        return records

    def _parse_item(self, item: dict) -> Optional[NormalizedDiscoveryRecord]:
        """Parses a single Semantic Scholar JSON paper object."""
        paper_id = item.get("paperId")
        title = item.get("title")
        if not paper_id or not title:
            return None
        title = " ".join(title.strip().split())

        # External IDs
        ext_ids = item.get("externalIds") or {}
        raw_doi = ext_ids.get("DOI")
        doi = normalize_doi(raw_doi) if raw_doi else None

        raw_arxiv = ext_ids.get("ArXiv")
        arxiv_id = normalize_arxiv_id(raw_arxiv) if raw_arxiv else None

        # Authors
        authors: List[str] = []
        for a in item.get("authors") or []:
            name = a.get("name")
            if name:
                authors.append(name.strip())

        # Abstract
        abstract = item.get("abstract")
        if abstract:
            abstract = " ".join(abstract.strip().split())

        # Venue
        venue = item.get("venue")
        if not venue and item.get("journal"):
            venue = item.get("journal", {}).get("name")

        # Dates
        pub_date: Optional[date] = None
        pub_date_str = item.get("publicationDate")
        if pub_date_str:
            try:
                pub_date = date.fromisoformat(pub_date_str)
            except Exception:
                pass

        pub_year = item.get("year")

        # URLs
        if doi:
            canonical_url = f"https://doi.org/{doi}"
        elif arxiv_id:
            canonical_url = f"https://arxiv.org/abs/{arxiv_id}"
        else:
            canonical_url = item.get("url") or f"https://www.semanticscholar.org/paper/{paper_id}"

        observed_url = item.get("url") or f"https://www.semanticscholar.org/paper/{paper_id}"

        # External IDs mapping
        external_ids = {k.lower(): str(v) for k, v in ext_ids.items() if v}
        external_ids["s2_paper_id"] = paper_id
        if item.get("corpusId"):
            external_ids["corpus_id"] = str(item["corpusId"])

        provider_metadata = {
            "paperId": paper_id,
            "corpusId": item.get("corpusId"),
            "doi": doi,
            "arxiv_id": arxiv_id,
            "citationCount": item.get("citationCount"),
            "influentialCitationCount": item.get("influentialCitationCount"),
            "openAccessPdf": item.get("openAccessPdf"),
        }

        return NormalizedDiscoveryRecord(
            provider="semantic_scholar",
            provider_document_id=paper_id,
            title=title,
            authors=authors,
            doi=doi,
            arxiv_id=arxiv_id,
            canonical_url=canonical_url,
            observed_url=observed_url,
            publication_date=pub_date,
            publication_year=pub_year,
            venue=venue,
            abstract=abstract,
            external_ids=external_ids,
            provider_metadata=provider_metadata,
        )
