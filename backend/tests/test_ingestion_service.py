"""Unit and Integration tests for IngestionService and BackgroundJob telemetry."""

from typing import Any, AsyncIterator, List, Optional
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from intel_os.connectors.base import BaseConnector
from intel_os.db.models.background_job import BackgroundJob
from intel_os.db.models.enums import JobStatus
from intel_os.db.models.source import Source
from intel_os.db.models.topic import Topic
from intel_os.ingestion.dto import NormalizedDiscoveryRecord
from intel_os.ingestion.service import IngestionService


class MockConnector(BaseConnector):
    """Mock connector generating synthetic test records."""

    name: str = "mock_provider"

    def __init__(self, count: int = 5, fail: bool = False) -> None:
        self.count = count
        self.fail = fail

    async def search(self, query: str, limit: int = 10, offset: int = 0, **kwargs: Any) -> List[NormalizedDiscoveryRecord]:
        if self.fail:
            raise RuntimeError("Provider API unreachable (Simulated 500 error)")

        records = []
        for i in range(offset, min(offset + limit, self.count)):
            doi = f"10.1000/mock.paper.{i}"
            records.append(
                NormalizedDiscoveryRecord(
                    provider="mock_provider",
                    provider_document_id=f"doc_{i}",
                    title=f"Mock Scientific Study #{i}",
                    authors=["Author A", "Author B"],
                    doi=doi,
                    canonical_url=f"https://doi.org/{doi}",
                    observed_url=f"https://mock.example.com/doc/{i}",
                )
            )
        return records

    async def fetch_by_id(self, identifier: str) -> Optional[NormalizedDiscoveryRecord]:
        return None


@pytest.mark.asyncio
async def test_ingestion_service_telemetry_and_bounds(db_session: AsyncSession):
    """Verify IngestionService executes bounded collection and accurately tracks BackgroundJob telemetry."""
    source = Source(name="Mock Source", source_type="academic_api", base_url="https://mock.example.com")
    topic = Topic(name="AI Verification", slug="ai-verification")
    db_session.add_all([source, topic])
    await db_session.flush()

    connector = MockConnector(count=5)

    # Run Ingestion
    job = await IngestionService.run_ingestion_job(
        session=db_session,
        connector=connector,
        source=source,
        query="verification",
        topic_id=topic.id,
        max_records=5,
    )

    assert job.status == JobStatus.COMPLETED
    assert job.progress_percentage == 100.0
    assert job.completed_at is not None

    res = job.result
    assert res["records_seen"] == 5
    assert res["new_documents"] == 5
    assert res["matched_documents"] == 0
    assert res["observations_created"] == 5
    assert res["observations_skipped"] == 0
    assert res["duration_seconds"] >= 0.0

    # Verify Source last_crawled_at updated
    assert source.last_crawled_at is not None

    # Run Re-ingestion with same records (Idempotent job run)
    job_re = await IngestionService.run_ingestion_job(
        session=db_session,
        connector=connector,
        source=source,
        query="verification",
        topic_id=topic.id,
        max_records=5,
    )

    assert job_re.status == JobStatus.COMPLETED
    res_re = job_re.result
    assert res_re["records_seen"] == 5
    assert res_re["new_documents"] == 0
    assert res_re["matched_documents"] == 5
    assert res_re["observations_created"] == 0
    assert res_re["observations_skipped"] == 5


@pytest.mark.asyncio
async def test_ingestion_service_error_handling(db_session: AsyncSession):
    """Verify IngestionService marks job as FAILED and captures error message upon exception."""
    source = Source(name="Failing Source", source_type="academic_api", base_url="https://fail.example.com")
    db_session.add(source)
    await db_session.flush()

    failing_connector = MockConnector(count=5, fail=True)

    with pytest.raises(RuntimeError, match="Provider API unreachable"):
        await IngestionService.run_ingestion_job(
            session=db_session,
            connector=failing_connector,
            source=source,
            query="test",
            max_records=5,
        )

    # Inspect BackgroundJob status
    stmt = select(BackgroundJob).where(BackgroundJob.payload["provider"].as_string() == "Failing Source")
    res = await db_session.execute(stmt)
    job = res.scalar_one()

    assert job.status == JobStatus.FAILED
    assert "Provider API unreachable" in job.error_message
