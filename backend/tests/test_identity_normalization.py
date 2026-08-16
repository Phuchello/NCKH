"""Unit tests for Identity Normalization and Metadata Fingerprinting."""

import pytest

from intel_os.ingestion.identity import (
    compute_metadata_fingerprint,
    extract_arxiv_version,
    normalize_arxiv_id,
    normalize_doi,
)


def test_normalize_doi_cases():
    """Verify DOI normalization strips prefixes, trims, lowercases, and validates structure."""
    valid_cases = [
        ("https://doi.org/10.1145/3372278.3390678", "10.1145/3372278.3390678"),
        ("http://dx.doi.org/10.1007/S10551-019-04354-9", "10.1007/s10551-019-04354-9"),
        ("doi: 10.1016/j.artint.2020.103348", "10.1016/j.artint.2020.103348"),
        ("10.1038/nature12373.", "10.1038/nature12373"),
        ("  10.1109/CVPR.2018.00762  ", "10.1109/cvpr.2018.00762"),
    ]
    for raw, expected in valid_cases:
        assert normalize_doi(raw) == expected

    invalid_cases = [
        None,
        "",
        "not-a-doi",
        "https://example.com/paper/123",
        "12.1234/invalid",
    ]
    for raw in invalid_cases:
        assert normalize_doi(raw) is None


def test_normalize_arxiv_id_logical_coalescence():
    """Verify arXiv ID normalization strips versions, prefixes, URLs, and produces logical ID."""
    cases = [
        ("arXiv:2301.12345v2", "2301.12345"),
        ("https://arxiv.org/abs/2106.09685v1", "2106.09685"),
        ("https://arxiv.org/pdf/2106.09685.pdf", "2106.09685"),
        ("hep-th/9901001v3", "hep-th/9901001"),
        ("math.PR/0101001", "math.pr/0101001"),
        ("0704.0001", "0704.0001"),
        ("2301.12345", "2301.12345"),
    ]
    for raw, expected in cases:
        assert normalize_arxiv_id(raw) == expected

    invalid_cases = [
        None,
        "",
        "12345",
        "https://google.com",
    ]
    for raw in invalid_cases:
        assert normalize_arxiv_id(raw) is None


def test_extract_arxiv_version():
    """Verify extraction of version tag from raw arXiv identifiers."""
    assert extract_arxiv_version("arXiv:2301.12345v2") == "v2"
    assert extract_arxiv_version("https://arxiv.org/abs/2106.09685v1") == "v1"
    assert extract_arxiv_version("hep-th/9901001v3") == "v3"
    assert extract_arxiv_version("2301.12345") is None
    assert extract_arxiv_version(None) is None


def test_compute_metadata_fingerprint():
    """Verify deterministic SHA-256 computation and case/whitespace insensitivity."""
    title = "Attention Is All You Need"
    authors = ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"]
    venue = "Advances in Neural Information Processing Systems"
    year = 2017

    fp1 = compute_metadata_fingerprint(title, authors, venue, year)
    fp2 = compute_metadata_fingerprint(
        "  attention  is all   you need. ",
        ["Niki Parmar", "Ashish Vaswani", "Noam Shazeer"],  # Different order
        "ADVANCES IN NEURAL INFORMATION PROCESSING SYSTEMS",
        2017,
    )

    assert fp1 == fp2
    assert len(fp1) == 64

    # Different title produces different fingerprint
    fp_diff = compute_metadata_fingerprint("BERT: Pre-training of Deep Bidirectional Transformers", authors, venue, year)
    assert fp_diff != fp1
