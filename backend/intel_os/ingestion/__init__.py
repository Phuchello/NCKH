"""Ingestion Core Subsystem Package."""

from intel_os.ingestion.dto import NormalizedDiscoveryRecord
from intel_os.ingestion.identity import (
    compute_metadata_fingerprint,
    extract_arxiv_version,
    normalize_arxiv_id,
    normalize_doi,
)
from intel_os.ingestion.persistence import persist_discovery_record
from intel_os.ingestion.reconciliation import ReconciliationEngine
from intel_os.ingestion.service import IngestionService

__all__ = [
    "NormalizedDiscoveryRecord",
    "normalize_doi",
    "normalize_arxiv_id",
    "extract_arxiv_version",
    "compute_metadata_fingerprint",
    "ReconciliationEngine",
    "persist_discovery_record",
    "IngestionService",
]
