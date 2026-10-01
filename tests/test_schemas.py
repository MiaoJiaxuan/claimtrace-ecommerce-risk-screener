"""Test required fields and value constraints in the structured risk card."""

import pytest
from pydantic import ValidationError

from src.schemas import RiskCard


def valid_risk_card(**overrides: object) -> dict:
    payload = {
        "risk_level": "evidence_needed",
        "highlighted_claim": "每月只花9元",
        "reason": "The price claim needs supporting records.",
        "source_title": "Example case",
        "source_url": "https://example.invalid/case",
        "next_action": "Verify the current offer.",
        "confidence": 0.75,
        "abstain": False,
    }
    payload.update(overrides)
    return payload


def test_valid_risk_card_is_parsed_with_optional_source_fields() -> None:
    """Protects the valid result-card contract and nullable citation fields."""
    card = RiskCard.model_validate(
        valid_risk_card(source_title=None, source_url=None)
    )

    assert card.risk_level == "evidence_needed"
    assert card.source_title is None
    assert card.source_url is None
    assert card.confidence == 0.75


@pytest.mark.parametrize(
    "risk_level",
    ["unknown", "officially_approved", ""],
)
def test_invalid_risk_level_is_rejected(risk_level: str) -> None:
    """Prevents outputs outside the four supported routing labels."""
    with pytest.raises(ValidationError):
        RiskCard.model_validate(valid_risk_card(risk_level=risk_level))


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_confidence_outside_zero_to_one_is_rejected(confidence: float) -> None:
    """Keeps model confidence within the documented probability-like range."""
    with pytest.raises(ValidationError):
        RiskCard.model_validate(valid_risk_card(confidence=confidence))


def test_required_field_missing_is_rejected() -> None:
    """Prevents incomplete model cards from entering the UI pipeline."""
    payload = valid_risk_card()
    del payload["next_action"]

    with pytest.raises(ValidationError):
        RiskCard.model_validate(payload)
