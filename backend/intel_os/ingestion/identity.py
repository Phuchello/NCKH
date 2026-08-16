"""Identity Normalization and Metadata Fingerprinting Module.

Provides canonical normalizers for DOIs, arXiv IDs, and candidate metadata fingerprints.
"""

import hashlib
import re
from typing import Optional, Sequence

# DOI Regex: Standard Crossref/IDF pattern (starts with 10.xxxx/)
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$")

# DOI Prefix cleanup regex
DOI_PREFIX_PATTERN = re.compile(
    r"^(https?://(dx\.)?doi\.org/|doi:\s*|info:doi/)",
    re.IGNORECASE,
)

# arXiv Prefix cleanup regex
ARXIV_PREFIX_PATTERN = re.compile(
    r"^(https?://arxiv\.org/(abs|pdf)/|arxiv:\s*)",
    re.IGNORECASE,
)

# arXiv Version suffix pattern (e.g. 'v1', 'v2')
ARXIV_VERSION_PATTERN = re.compile(r"v\d+$", re.IGNORECASE)

# Old arXiv format: e.g. hep-th/9901001 or math.PR/0101001
OLD_ARXIV_PATTERN = re.compile(r"^[a-zA-Z\-]+(\.[a-zA-Z\-]+)?/\d{7}(v\d+)?$")

# New arXiv format: e.g. 2301.12345 or 0704.0001
NEW_ARXIV_PATTERN = re.compile(r"^\d{4}\.\d{4,5}(v\d+)?$")


def normalize_doi(doi: Optional[str]) -> Optional[str]:
    """Normalizes a DOI to its canonical lowercase string without URL prefixes.

    Examples:
        'https://doi.org/10.1145/3372278.3390678' -> '10.1145/3372278.3390678'
        '10.1007/S10551-019-04354-9' -> '10.1007/s10551-019-04354-9'
        'DOI: 10.1016/j.artint.2020.103348' -> '10.1016/j.artint.2020.103348'
    """
    if not doi or not isinstance(doi, str):
        return None

    cleaned = doi.strip()
    cleaned = DOI_PREFIX_PATTERN.sub("", cleaned).strip()

    # Remove trailing periods, slashes, or quotes occasionally added in scraped references
    cleaned = cleaned.rstrip("./\"' ")

    if not cleaned:
        return None

    cleaned_lower = cleaned.lower()

    if DOI_PATTERN.match(cleaned_lower):
        return cleaned_lower

    return None


def normalize_arxiv_id(arxiv_id: Optional[str]) -> Optional[str]:
    """Normalizes an arXiv identifier to its canonical logical identifier.

    Strips URLs, prefixes ('arXiv:'), and version suffixes ('v1', 'v2')
    so that all revisions map to the same logical work identity.

    Examples:
        'arXiv:2301.12345v2' -> '2301.12345'
        'https://arxiv.org/abs/2106.09685v1' -> '2106.09685'
        'hep-th/9901001v3' -> 'hep-th/9901001'
    """
    if not arxiv_id or not isinstance(arxiv_id, str):
        return None

    cleaned = arxiv_id.strip()
    cleaned = ARXIV_PREFIX_PATTERN.sub("", cleaned).strip()

    # Remove trailing .pdf extension if present
    if cleaned.lower().endswith(".pdf"):
        cleaned = cleaned[:-4].strip()

    if not cleaned:
        return None

    # Check for match against old or new format
    if NEW_ARXIV_PATTERN.match(cleaned) or OLD_ARXIV_PATTERN.match(cleaned):
        # Strip version suffix (e.g. 'v2') for logical identifier
        logical_id = ARXIV_VERSION_PATTERN.sub("", cleaned)
        return logical_id.lower()

    return None


def extract_arxiv_version(raw_arxiv_id: Optional[str]) -> Optional[str]:
    """Extracts the version tag from an arXiv identifier if present.

    Examples:
        '2301.12345v2' -> 'v2'
        '2301.12345' -> None
    """
    if not raw_arxiv_id or not isinstance(raw_arxiv_id, str):
        return None

    match = ARXIV_VERSION_PATTERN.search(raw_arxiv_id.strip())
    if match:
        return match.group(0).lower()
    return None


def _clean_text_for_fingerprint(text: str) -> str:
    """Collapses whitespace and strips punctuation for robust fingerprinting."""
    # Replace non-alphanumeric with space, lowercase, and collapse
    alphanumeric = re.sub(r"[^\w\s]", " ", text.lower())
    return " ".join(alphanumeric.split())


def compute_metadata_fingerprint(
    title: str,
    authors: Sequence[str],
    venue: Optional[str] = None,
    year: Optional[int] = None,
) -> str:
    """Computes a deterministic SHA-256 fingerprint for candidate document matching.

    Formula:
        sha256(cleaned_title + '|' + sorted_authors + '|' + cleaned_venue + '|' + year)
    """
    cleaned_title = _clean_text_for_fingerprint(title or "")

    # Clean and sort author names
    cleaned_authors = sorted(
        [_clean_text_for_fingerprint(a) for a in authors if a and a.strip()]
    )
    authors_str = ";".join(cleaned_authors)

    cleaned_venue = _clean_text_for_fingerprint(venue or "")
    year_str = str(year) if year else ""

    payload = f"{cleaned_title}|{authors_str}|{cleaned_venue}|{year_str}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
