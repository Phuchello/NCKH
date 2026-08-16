"""Enumeration types for Intel OS domain models."""

import enum


class RetentionTier(str, enum.Enum):
    """Retention tier for documents & snapshots in Intelligence Lake."""

    DISCOVERED = "DISCOVERED"  # Metadata only (Title, DOI, Authors, Venue, URL)
    INDEXED = "INDEXED"  # Metadata + Abstract + fast embeddings
    RELEVANT = "RELEVANT"  # Full parsed text & structural sections
    RETAINED = "RETAINED"  # Raw PDF/HTML preserved in S3 Object Storage
    ARCHIVED = "ARCHIVED"  # Deep cold storage backup


class GroundingStatus(str, enum.Enum):
    """Grounding status: Verifies text presence in source, NOT scientific validity."""

    UNVERIFIED = "UNVERIFIED"  # Extracted claim has not completed quote verification
    VERBATIM_MATCH = "VERBATIM_MATCH"  # Statement matches exact character substring
    PARAPHRASE_VERIFIED = "PARAPHRASE_VERIFIED"  # Meaning verified against bounding quotes
    FAILED = "FAILED"  # Quote does not exist in source text (discarded/quarantined)


class ClaimType(str, enum.Enum):
    """Claim type classification."""

    EMPIRICAL_FINDING = "EMPIRICAL_FINDING"  # Quantitative/experimental result
    AUTHOR_HYPOTHESIS = "AUTHOR_HYPOTHESIS"  # Proposition formulated by author
    BACKGROUND_ASSERTION = "BACKGROUND_ASSERTION"  # Stated as prior literature
    INTERPRETATION = "INTERPRETATION"  # Qualitative deduction / explanation
    LIMITATION = "LIMITATION"  # Stated boundary condition or failure mode
    FUTURE_WORK = "FUTURE_WORK"  # Suggested research direction
    OTHER = "OTHER"  # Uncategorized statement


class EpistemicStatus(str, enum.Enum):
    """Epistemic status: Reflects scientific validity & consensus across literature."""

    UNASSESSED = "UNASSESSED"  # Default upon extraction; no validity judgment yet
    SUPPORTED = "SUPPORTED"  # Validated by rigorous methodology/replication
    CONTESTED = "CONTESTED"  # Direct conflicting finding identified
    REFUTED = "REFUTED"  # Methodologically invalid or disproven
    CONSENSUS = "CONSENSUS"  # Established scientific consensus
    SPECULATIVE = "SPECULATIVE"  # Untested hypothesis or theoretical conjecture


class IdeaStatus(str, enum.Enum):
    """Idea status in Opportunity Bank."""

    CANDIDATE = "CANDIDATE"  # Automatically generated proposal
    REVIEWED = "REVIEWED"  # Evaluated by human researcher
    ACCEPTED = "ACCEPTED"  # Approved for active research
    REJECTED = "REJECTED"  # Deemed infeasible or duplicate
    ARCHIVED = "ARCHIVED"  # Historical reference


class JobStatus(str, enum.Enum):
    """Background job execution status."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
