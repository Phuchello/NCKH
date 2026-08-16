"""arXiv Scholarly API Connector.

Connects to the official arXiv Atom 1.0 XML Query API, enforces the mandatory 3-second
inter-request delay, and extracts canonical logical vs versioned arXiv metadata.
"""

from datetime import date, datetime
from typing import Any, List, Optional
import xml.etree.ElementTree as ET

from intel_os.connectors.base import BaseConnector
from intel_os.core.config import get_settings
from intel_os.core.logging import get_logger
from intel_os.http.rate_limit import RateLimiter
from intel_os.http.transport import ResilientHttpClient
from intel_os.ingestion.dto import NormalizedDiscoveryRecord
from intel_os.ingestion.identity import extract_arxiv_version, normalize_arxiv_id, normalize_doi

logger = get_logger(__name__)

# Atom XML Namespaces used by arXiv
ATOM_NS = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"


class ArxivConnector(BaseConnector):
    """Connector for the arXiv API (Atom 1.0 XML)."""

    name: str = "arxiv"
    source_type: str = "academic_repo"
    base_url: str = "https://export.arxiv.org/api/query"

    def __init__(self, http_client: Optional[ResilientHttpClient] = None) -> None:
        settings = get_settings()
        rate_limiter = RateLimiter(
            name="arxiv",
            min_delay_seconds=settings.ARXIV_RATE_LIMIT_DELAY_SECONDS,
            max_concurrency=1,
        )
        client = http_client or ResilientHttpClient(
            name="arxiv",
            rate_limiter=rate_limiter,
        )
        super().__init__(http_client=client)

    async def search(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
        **kwargs: Any,
    ) -> List[NormalizedDiscoveryRecord]:
        """Searches arXiv by keyword or category."""
        params = {
            "search_query": query,
            "start": offset,
            "max_results": limit,
            "sortBy": kwargs.get("sortBy", "relevance"),
            "sortOrder": kwargs.get("sortOrder", "descending"),
        }
        response = await self.http_client.get(self.base_url, params=params)
        response.raise_for_status()
        return self._parse_feed(response.text)

    async def fetch_by_id(self, identifier: str) -> Optional[NormalizedDiscoveryRecord]:
        """Fetches a single paper by arXiv ID."""
        clean_id = normalize_arxiv_id(identifier) or identifier.strip()
        params = {
            "id_list": clean_id,
            "start": 0,
            "max_results": 1,
        }
        response = await self.http_client.get(self.base_url, params=params)
        response.raise_for_status()
        records = self._parse_feed(response.text)
        return records[0] if records else None

    def _parse_feed(self, xml_content: str) -> List[NormalizedDiscoveryRecord]:
        """Parses Atom 1.0 XML response into NormalizedDiscoveryRecord instances."""
        if not xml_content or not xml_content.strip():
            return []

        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as exc:
            logger.warning(f"Failed to parse arXiv XML payload: {exc}")
            return []

        records: List[NormalizedDiscoveryRecord] = []

        for entry in root.findall(f"{ATOM_NS}entry"):
            try:
                record = self._parse_entry(entry)
                if record:
                    records.append(record)
            except Exception as exc:
                logger.warning(f"Error parsing arXiv entry: {exc}", exc_info=True)
                continue

        return records

    def _parse_entry(self, entry: ET.Element) -> Optional[NormalizedDiscoveryRecord]:
        """Parses a single XML <entry> element."""
        id_elem = entry.find(f"{ATOM_NS}id")
        title_elem = entry.find(f"{ATOM_NS}title")

        if id_elem is None or not id_elem.text or title_elem is None or not title_elem.text:
            return None

        raw_id_url = id_elem.text.strip()
        # Raw ID typically looks like: http://arxiv.org/abs/2301.12345v1
        raw_arxiv_id = raw_id_url.rsplit("/", 1)[-1]
        logical_arxiv_id = normalize_arxiv_id(raw_arxiv_id) or raw_arxiv_id
        version_tag = extract_arxiv_version(raw_arxiv_id)

        # Clean title (arXiv titles often contain newlines)
        title = " ".join(title_elem.text.strip().split())

        # Extract authors
        authors: List[str] = []
        for author_elem in entry.findall(f"{ATOM_NS}author"):
            name_elem = author_elem.find(f"{ATOM_NS}name")
            if name_elem is not None and name_elem.text:
                authors.append(name_elem.text.strip())

        # Extract abstract (summary)
        summary_elem = entry.find(f"{ATOM_NS}summary")
        abstract = None
        if summary_elem is not None and summary_elem.text:
            abstract = " ".join(summary_elem.text.strip().split())

        # Extract publication date
        published_elem = entry.find(f"{ATOM_NS}published")
        pub_date: Optional[date] = None
        pub_year: Optional[int] = None
        if published_elem is not None and published_elem.text:
            try:
                dt = datetime.fromisoformat(published_elem.text.strip().replace("Z", "+00:00"))
                pub_date = dt.date()
                pub_year = dt.year
            except Exception:
                pass

        # Extract DOI if present in arxiv:doi
        doi_elem = entry.find(f"{ARXIV_NS}doi")
        doi = None
        if doi_elem is not None and doi_elem.text:
            doi = normalize_doi(doi_elem.text.strip())

        # Extract venue / journal_ref
        journal_elem = entry.find(f"{ARXIV_NS}journal_ref")
        venue = journal_elem.text.strip() if journal_elem is not None and journal_elem.text else f"arXiv:{logical_arxiv_id}"

        # Canonical landing page URL
        canonical_url = f"https://arxiv.org/abs/{logical_arxiv_id}"

        # External IDs
        external_ids = {
            "arxiv": logical_arxiv_id,
        }
        if version_tag:
            external_ids["arxiv_version"] = version_tag
        if doi:
            external_ids["doi"] = doi

        # Raw provider metadata dictionary
        provider_metadata = {
            "arxiv_id": logical_arxiv_id,
            "raw_id": raw_arxiv_id,
            "version": version_tag,
            "published": published_elem.text.strip() if published_elem is not None and published_elem.text else None,
            "doi": doi,
            "journal_ref": venue,
        }

        return NormalizedDiscoveryRecord(
            provider="arxiv",
            provider_document_id=logical_arxiv_id,
            title=title,
            authors=authors,
            doi=doi,
            arxiv_id=logical_arxiv_id,
            canonical_url=canonical_url,
            observed_url=raw_id_url,
            publication_date=pub_date,
            publication_year=pub_year,
            venue=venue,
            abstract=abstract,
            external_ids=external_ids,
            provider_metadata=provider_metadata,
        )
