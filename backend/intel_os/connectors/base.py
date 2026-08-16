"""Base Connector Abstract Class for Scholarly Ingestion Feeds."""

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, List, Optional

from intel_os.http.transport import ResilientHttpClient
from intel_os.ingestion.dto import NormalizedDiscoveryRecord


class BaseConnector(ABC):
    """Abstract Base Class for all academic repository and index connectors."""

    name: str = "base"
    source_type: str = "academic_api"
    base_url: str = ""

    def __init__(self, http_client: Optional[ResilientHttpClient] = None) -> None:
        """Initializes the connector with a resilient HTTP transport client."""
        self.http_client = http_client or ResilientHttpClient(name=self.name)

    @abstractmethod
    async def search(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
        **kwargs: Any,
    ) -> List[NormalizedDiscoveryRecord]:
        """Performs a single paginated search query against the provider API."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_by_id(self, identifier: str) -> Optional[NormalizedDiscoveryRecord]:
        """Fetches a single work by its primary canonical identifier (DOI, arXiv ID, or provider ID)."""
        raise NotImplementedError

    async def stream(
        self,
        query: str,
        max_records: int = 50,
        page_size: int = 20,
        **kwargs: Any,
    ) -> AsyncIterator[NormalizedDiscoveryRecord]:
        """Streams normalized discovery records up to max_records, handling pagination.

        Guarantees loop termination on empty results or when page size limit is reached.
        """
        offset = 0
        yielded = 0

        while yielded < max_records:
            current_limit = min(page_size, max_records - yielded)
            records = await self.search(query=query, limit=current_limit, offset=offset, **kwargs)

            if not records:
                break

            for record in records:
                yield record
                yielded += 1
                if yielded >= max_records:
                    break

            if len(records) < current_limit:
                # Provider returned fewer items than requested; end of pagination
                break

            offset += len(records)

    async def close(self) -> None:
        """Closes the underlying HTTP client session."""
        await self.http_client.close()

    async def __aenter__(self) -> "BaseConnector":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
