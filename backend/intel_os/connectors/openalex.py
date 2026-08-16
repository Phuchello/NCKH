"""OpenAlex Scholarly Works REST API Connector.

Connects to the official OpenAlex Works API, reconstructs abstracts from inverted indices,
and extracts rich author and concept metadata.
"""

from datetime import date
from typing import Any, List, Optional

from intel_os.connectors.base import BaseConnector
from intel_os.core.config import get_settings
from intel_os.core.logging import get_logger
from intel_os.http.rate_limit import RateLimiter
from intel_os.http.transport import ResilientHttpClient
from intel_os.ingestion.dto import NormalizedDiscoveryRecord
from intel_os.ingestion.identity import normalize_doi

logger = get_logger(__name__)


def reconstruct_inverted_abstract(inverted_index: Optional[dict[str, list[int]]]) -> Optional[str]:
    """Reconstructs full text abstract from OpenAlex's abstract_inverted_index dictionary."""
    if not inverted_index or not isinstance(inverted_index, dict):
        return None

    # Determine max index length
    words_by_pos: dict[int, str] = {}
    for word, positions in inverted_index.items():
        for pos in positions:
            words_by_pos[pos] = word

    if not words_by_pos:
        return None

    max_pos = max(words_by_pos.keys())
    ordered_words = [words_by_pos.get(i, "") for i in range(max_pos + 1)]
    abstract = " ".join(ordered_words).strip()
    return " ".join(abstract.split()) if abstract else None


class OpenAlexConnector(BaseConnector):
    """Connector for OpenAlex Works API."""

    name: str = "openalex"
    source_type: str = "open_index"
    base_url: str = "https://api.openalex.org/works"

    def __init__(self, http_client: Optional[ResilientHttpClient] = None) -> None:
        settings = get_settings()
        rate_limiter = RateLimiter(
            name="openalex",
            rps=settings.OPENALEX_RATE_LIMIT_RPS,
            max_burst=5,
            max_concurrency=settings.HTTP_MAX_CONCURRENCY_PER_HOST,
        )
        headers = {
            "User-Agent": settings.INGEST_USER_AGENT,
        }
        client = http_client or ResilientHttpClient(
            name="openalex",
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
        """Searches OpenAlex works by keyword search."""
        settings = get_settings()
        # OpenAlex uses 1-indexed page or cursor
        page = (offset // max(1, limit)) + 1
        params: dict[str, Any] = {
            "search": query,
            "per-page": limit,
            "page": page,
            "mailto": settings.INGEST_POLITE_EMAIL,
        }
        if "filter" in kwargs:
            params["filter"] = kwargs["filter"]
        if "sort" in kwargs:
            params["sort"] = kwargs["sort"]

        response = await self.http_client.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        return self._parse_results(results)

    async def fetch_by_id(self, identifier: str) -> Optional[NormalizedDiscoveryRecord]:
        """Fetches a single work by OpenAlex ID or DOI."""
        settings = get_settings()
        clean_id = identifier.strip()
        url = f"{self.base_url}/{clean_id}"
        params = {"mailto": settings.INGEST_POLITE_EMAIL}
        response = await self.http_client.get(url, params=params)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        item = response.json()
        return self._parse_item(item)

    def _parse_results(self, results: List[dict]) -> List[NormalizedDiscoveryRecord]:
        """Parses list of OpenAlex work dictionaries."""
        records: List[NormalizedDiscoveryRecord] = []
        for item in results:
            try:
                record = self._parse_item(item)
                if record:
                    records.append(record)
            except Exception as exc:
                logger.warning(f"Error parsing OpenAlex work: {exc}", exc_info=True)
                continue
        return records

    def _parse_item(self, item: dict) -> Optional[NormalizedDiscoveryRecord]:
        """Parses a single OpenAlex JSON work object."""
        raw_id = item.get("id", "")
        # Strip URL prefix if present (e.g. 'https://openalex.org/W2741809807' -> 'W2741809807')
        openalex_id = raw_id.rsplit("/", 1)[-1] if raw_id else None

        title = item.get("title") or item.get("display_name")
        if not title:
            return None
        title = " ".join(title.strip().split())

        # DOI
        raw_doi = item.get("doi")
        doi = normalize_doi(raw_doi) if raw_doi else None

        # Authors
        authors: List[str] = []
        for authorship in item.get("authorships", []):
            author = authorship.get("author", {})
            name = author.get("display_name")
            if name:
                authors.append(name.strip())

        # Abstract
        abstract = reconstruct_inverted_abstract(item.get("abstract_inverted_index"))

        # Venue
        venue = None
        primary_loc = item.get("primary_location") or {}
        source_obj = primary_loc.get("source") or {}
        if source_obj and source_obj.get("display_name"):
            venue = source_obj["display_name"].strip()

        # Dates
        pub_date: Optional[date] = None
        pub_date_str = item.get("publication_date")
        if pub_date_str:
            try:
                pub_date = date.fromisoformat(pub_date_str)
            except Exception:
                pass

        pub_year = item.get("publication_year")

        # URLs
        canonical_url = f"https://doi.org/{doi}" if doi else (item.get("doi") or f"https://openalex.org/{openalex_id}")
        observed_url = item.get("id") or canonical_url

        # External IDs
        external_ids = {}
        if openalex_id:
            external_ids["openalex"] = openalex_id
        if doi:
            external_ids["doi"] = doi
        ids_obj = item.get("ids", {})
        if "mag" in ids_obj:
            external_ids["mag"] = str(ids_obj["mag"])
        if "pmid" in ids_obj:
            external_ids["pmid"] = str(ids_obj["pmid"])

        provider_metadata = {
            "openalex_id": openalex_id,
            "doi": doi,
            "cited_by_count": item.get("cited_by_count"),
            "concepts": [c.get("display_name") for c in item.get("concepts", [])[:5] if c.get("display_name")],
            "is_oa": item.get("open_access", {}).get("is_oa"),
            "oa_url": item.get("open_access", {}).get("oa_url"),
        }

        return NormalizedDiscoveryRecord(
            provider="openalex",
            provider_document_id=openalex_id,
            title=title,
            authors=authors,
            doi=doi,
            arxiv_id=None,
            canonical_url=canonical_url,
            observed_url=observed_url,
            publication_date=pub_date,
            publication_year=pub_year,
            venue=venue,
            abstract=abstract,
            external_ids=external_ids,
            provider_metadata=provider_metadata,
        )
