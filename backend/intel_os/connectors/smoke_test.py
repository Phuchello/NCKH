"""Optional Live Academic API Smoke Test Runner.

DISABLED BY DEFAULT. Does not run in automated CI.
Requires explicit opt-in via environment variable `LIVE_SMOKE_TEST=1` or `--live` flag.
Executes minimal, polite, 1-record queries across active scholarly providers.
"""

import asyncio
import os
import sys

from intel_os.connectors.arxiv import ArxivConnector
from intel_os.connectors.crossref import CrossrefConnector
from intel_os.connectors.openalex import OpenAlexConnector
from intel_os.connectors.semantic_scholar import SemanticScholarConnector
from intel_os.core.logging import get_logger, setup_logging

logger = get_logger("smoke_test")


async def run_live_smoke_test() -> None:
    """Executes 1-record live smoke test across all 4 scholarly providers."""
    setup_logging(level="INFO")
    print("=" * 70)
    print("INTEL OS / NCKH — OPTIONAL LIVE SCHOLARLY API SMOKE TEST")
    print("=" * 70)

    # 1. arXiv Live Smoke
    print("\n[1/4] Probing arXiv API...")
    async with ArxivConnector() as arxiv_conn:
        arxiv_recs = await arxiv_conn.search(query="cat:cs.AI", limit=1)
        if arxiv_recs:
            print(f"  ✓ arXiv OK: '{arxiv_recs[0].title[:50]}...' ({arxiv_recs[0].canonical_url})")
        else:
            print("  ✗ arXiv returned 0 records.")

    # 2. Crossref Live Smoke
    print("\n[2/4] Probing Crossref Works API...")
    async with CrossrefConnector() as crossref_conn:
        crossref_recs = await crossref_conn.search(query="deep learning", limit=1)
        if crossref_recs:
            print(f"  ✓ Crossref OK: '{crossref_recs[0].title[:50]}...' (DOI: {crossref_recs[0].doi})")
        else:
            print("  ✗ Crossref returned 0 records.")

    # 3. OpenAlex Live Smoke
    print("\n[3/4] Probing OpenAlex Works API...")
    async with OpenAlexConnector() as openalex_conn:
        openalex_recs = await openalex_conn.search(query="graph neural networks", limit=1)
        if openalex_recs:
            print(f"  ✓ OpenAlex OK: '{openalex_recs[0].title[:50]}...' (ID: {openalex_recs[0].provider_document_id})")
        else:
            print("  ✗ OpenAlex returned 0 records.")

    # 4. Semantic Scholar Live Smoke
    print("\n[4/4] Probing Semantic Scholar Academic Graph API...")
    async with SemanticScholarConnector() as s2_conn:
        s2_recs = await s2_conn.search(query="transformers language model", limit=1)
        if s2_recs:
            print(f"  ✓ Semantic Scholar OK: '{s2_recs[0].title[:50]}...' (S2 Paper ID: {s2_recs[0].provider_document_id})")
        else:
            print("  ✗ Semantic Scholar returned 0 records.")

    print("\n" + "=" * 70)
    print("LIVE SMOKE TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    is_live = os.getenv("LIVE_SMOKE_TEST") == "1" or "--live" in sys.argv
    if not is_live:
        print("Live smoke test is disabled by default.")
        print("To run live test against academic APIs, execute: python -m intel_os.connectors.smoke_test --live")
        sys.exit(0)

    asyncio.run(run_live_smoke_test())
