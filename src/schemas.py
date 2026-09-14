from typing import Literal, Optional

from pydantic import BaseModel, Field


class RiskCard(BaseModel):
    """Structured output returned by the LLM assessment."""

    risk_level: Literal[
        "high_risk",
        "evidence_needed",
        "low_risk",
        "insufficient_evidence",
    ]

    highlighted_claim: str
    reason: str
    source_title: Optional[str] = None
    source_url: Optional[str] = None
    next_action: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    abstain: bool