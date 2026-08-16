"""Crossref Scholarly Works REST API Connector.

Connects to the official Crossref Works API, enforces Polite Pool headers,
and normalizes DOIs, JATS abstracts, and citation metadata.
"""

from datetime import date
import re
from typing import Any, List, Optional

from intel_os.connectors.base import BaseConnector
from intel_os.core.config import get_settings
from intel_os.core.logging import get_logger
from intel_os.http.rate_limit import RateLimiter
from intel_os.http.transport import ResilientHttpClient
from intel_os.ingestion.dto import NormalizedDiscoveryRecord
from intel_os.ingestion.identity import normalize_doi

logger = get_logger(__name__)

# Regex for stripping JATS XML tags from Crossref abstracts
JATS_TAG_PATTERN = re.compile(r"<[^>]+>")


def clean_jats_abstract(abstract_raw: Optional[str]) -> Optional[str]:
    """Strips XML/JATS markup from Crossref abstract strings."""
    if not abstract_raw or not isinstance(abstract_raw, str):
        return None
    cleaned = JATS_TAG_PATTERN.sub("", abstract_raw)
    return " ".join(cleaned.split())


class CrossrefConnector(BaseConnector):
    """Connector for Crossref REST API."""

    name: str = "crossref"
    source_type: str = "doi_registry"
    base_url: str = "https://api.crossref.org/works"

    def __init__(self, http_client: Optional[ResilientHttpClient] = None) -> None:
        settings = get_settings()
        rate_limiter = RateLimiter(
            name="crossref",
            rps=settings.CROSSREF_RATE_LIMIT_RPS,
            max_burst=5,
            max_concurrency=settings.HTTP_MAX_CONCURRENCY_PER_HOST,
        )
        headers = {
            "User-Agent": settings.INGEST_USER_AGENT,
            "mailto": settings.INGEST_POLITE_EMAIL,
        }
        client = http_client or ResilientHttpClient(
            name="crossref",
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
        """Searches Crossref works by bibliographic query."""
        settings = get_settings()
        params: dict[str, Any] = {
            "query": query,
            "rows": limit,
            "offset": offset,
            "mailto": settings.INGEST_POLITE_EMAIL,
        }
        if "filter" in kwargs:
            params["filter"] = kwargs["filter"]
        if "sort" in kwargs:
            params["sort"] = kwargs["sort"]

        response = await self.http_client.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        items = data.get("message", {}).get("items", [])
        return self._parse_items(items)

    async def fetch_by_id(self, identifier: str) -> Optional[NormalizedDiscoveryRecord]:
        """Fetches a single work by DOI."""
        clean_doi = normalize_doi(identifier) or identifier.strip()
        url = f"{self.base_url}/{clean_doi}"
        response = await self.http_client.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
        item = data.get("message")
        if not item:
            return None
        return self._parse_item(item)

    def _parse_items(self, items: List[dict]) -> List[NormalizedDiscoveryRecord]:
        """Parses list of Crossref work items."""
        records: List[NormalizedDiscoveryRecord] = []
        for item in items:
            try:
                record = self._parse_item(item)
                if record:
                    records.append(record)
            except Exception as exc:
                logger.warning(f"Error parsing Crossref item: {exc}", exc_info=True)
                continue
        return records

    def _parse_item(self, item: dict) -> Optional[NormalizedDiscoveryRecord]:
        """Parses a single Crossref JSON item."""
        raw_doi = item.get("DOI")
        doi = normalize_doi(raw_doi) if raw_doi else None

        # Title parsing
        titles = item.get("title", [])
        title = " ".join(titles[0].strip().split()) if titles and titles[0] else None
        if not title:
            return None

        # Authors parsing
        authors: List[str] = []
        for a in item.get("author", []):
            if "name" in a and a["name"]:
                authors.append(a["name"].strip())
            else:
                given = a.get("given", "").strip()
                family = a.get("family", "").strip()
                name = f"{given} {family}".strip()
                if name:
                    authors.append(name)

        # Abstract
        abstract = clean_jats_abstract(item.get("abstract"))

        # Venue
        container_titles = item.get("container-title", [])
        venue = container_titles[0].strip() if container_titles and container_titles[0] else None

        # Publication date / year
        pub_date: Optional[date] = None
        pub_year: Optional[int] = None
        date_parts = None
        for key in ("published-online", "published-print", "issued", "created"):
            parts = item.get(key, {}).get("date-parts")
            if parts and len(parts) > 0 and len(parts[0]) > 0:
                date_parts = parts[0]
                break

        if date_parts:
            try:
                year = int(date_parts[0])
                month = int(date_parts[1]) if len(date_parts) > 1 else 1
                day = int(date_parts[2]) if len(date_parts) > 2 else 1
                pub_date = date(year, month, day)
                pub_year = year
            except Exception:
                if len(date_parts) > 0:
                    try:
                        pub_year = int(date_parts[0])
                    except Exception:
                        pass

        # Canonical & Observed URLs
        canonical_url = f"https://doi.org/{doi}" if doi else item.get("URL", f"https://api.crossref.org/works/{raw_doi}")
        observed_url = item.get("URL", canonical_url)

        external_ids = {}
        if doi:
            external_ids["doi"] = doi

        provider_metadata = {
            "doi": doi,
            "type": item.get("type"),
            "publisher": item.get("publisher"),
            "is_referenced_by_count": item.get("is-referenced-by-count"),
            "container_title": venue,
        }

        return NormalizedDiscoveryRecord(
            provider="crossref",
            provider_document_id=doi,
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
