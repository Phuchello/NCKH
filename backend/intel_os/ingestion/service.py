"""Ingestion Orchestrator Service.

Coordinates collection runs across scholarly connectors, executes persistence,
and updates BackgroundJob execution telemetry.
"""

from datetime import datetime
import time
from typing import TYPE_CHECKING, Any, Optional
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from intel_os.core.logging import get_logger
from intel_os.db.base import utc_now
from intel_os.db.models.background_job import BackgroundJob
from intel_os.db.models.enums import JobStatus
from intel_os.db.models.source import Source
from intel_os.ingestion.persistence import persist_discovery_record

if TYPE_CHECKING:
    from intel_os.connectors.base import BaseConnector

logger = get_logger(__name__)


class IngestionService:
    """Orchestrates discovery and ingestion across scholarly sources."""

    @staticmethod
    async def run_ingestion_job(
        session: AsyncSession,
        connector: "BaseConnector",
        source: Source,
        query: str,
        topic_id: Optional[uuid.UUID] = None,
        max_records: int = 50,
        job_id: Optional[uuid.UUID] = None,
        idempotency_key: Optional[str] = None,
    ) -> BackgroundJob:
        """Executes a bounded ingestion harvest and records job telemetry."""
        # 1. Initialize or load BackgroundJob
        job: Optional[BackgroundJob] = None
        if job_id:
            job = await session.get(BackgroundJob, job_id)
        elif idempotency_key:
            stmt = select(BackgroundJob).where(BackgroundJob.idempotency_key == idempotency_key)
            res = await session.execute(stmt)
            job = res.scalar_one_or_none()

        if job is None:
            auto_key = idempotency_key or f"ingest:{source.name}:{query}:{uuid.uuid4().hex[:8]}"
            job = BackgroundJob(
                job_type="academic_ingest",
                idempotency_key=auto_key,
                status=JobStatus.RUNNING,
                payload={
                    "provider": source.name,
                    "query": query,
                    "topic_id": str(topic_id) if topic_id else None,
                    "max_records": max_records,
                },
                started_at=utc_now(),
            )
            session.add(job)
            await session.flush()
        else:
            job.status = JobStatus.RUNNING
            job.started_at = utc_now()
            await session.flush()

        start_time = time.monotonic()
        records_seen = 0
        new_docs = 0
        matched_docs = 0
        obs_created = 0
        obs_skipped = 0

        try:
            async for record in connector.stream(query, max_records=max_records):
                records_seen += 1

                doc, doc_source, is_new_doc, is_new_obs = await persist_discovery_record(
                    session=session,
                    record=record,
                    source_id=source.id,
                    topic_id=topic_id,
                )

                if is_new_doc:
                    new_docs += 1
                else:
                    matched_docs += 1

                if is_new_obs:
                    obs_created += 1
                else:
                    obs_skipped += 1

                # Update progress percentage
                if max_records > 0:
                    job.progress_percentage = min(100.0, (records_seen / max_records) * 100.0)

            # Update Source timestamp
            source.last_crawled_at = utc_now()

            # Finalize Job Telemetry
            duration = time.monotonic() - start_time
            job.status = JobStatus.COMPLETED
            job.progress_percentage = 100.0
            job.completed_at = utc_now()
            job.result = {
                "records_seen": records_seen,
                "new_documents": new_docs,
                "matched_documents": matched_docs,
                "observations_created": obs_created,
                "observations_skipped": obs_skipped,
                "duration_seconds": round(duration, 3),
            }
            await session.commit()
            return job

        except Exception as exc:
            duration = time.monotonic() - start_time
            logger.error(f"Ingestion job failed for {source.name} query='{query}': {exc}", exc_info=True)
            job.status = JobStatus.FAILED
            job.error_message = str(exc)
            job.completed_at = utc_now()
            job.result = {
                "records_seen": records_seen,
                "new_documents": new_docs,
                "matched_documents": matched_docs,
                "observations_created": obs_created,
                "observations_skipped": obs_skipped,
                "duration_seconds": round(duration, 3),
            }
            await session.commit()
            raise
