"""Test configured rule labels and the transparent baseline boundary."""

import pytest

from src.rules_baseline import assess_by_rules, find_matches


def test_empty_claim_returns_insufficient_evidence_and_no_matches() -> None:
    """Prevents blank input from being presented as a low-risk assessment."""
    result = assess_by_rules("  \n")

    assert result["risk_level"] == "insufficient_evidence"
    assert result["matched_terms"] == []
    assert result["method"] == "rules_baseline"


@pytest.mark.parametrize("claim", ["彻底治愈", "国家级品质", "效果最佳"])
def test_high_risk_patterns_are_flagged(claim: str) -> None:
    """Protects escalation for configured cure and absolute-superlative claims."""
    result = assess_by_rules(claim)

    assert result["risk_level"] == "high_risk"
    assert result["matched_terms"]
    assert "human review" in result["next_action"].lower()


@pytest.mark.parametrize("claim", ["每月9元", "销量第一", "有效改善肤质"])
def test_evidence_patterns_request_supporting_records(claim: str) -> None:
    """Ensures factual price, ranking, and effect claims request evidence."""
    result = assess_by_rules(claim)

    assert result["risk_level"] == "evidence_needed"
    assert result["matched_terms"]
    assert "records" in result["next_action"].lower()


def test_high_risk_takes_precedence_but_keeps_evidence_matches() -> None:
    """Keeps high-risk escalation dominant without discarding matched evidence terms."""
    result = assess_by_rules("每月9元，保证彻底治愈")

    assert result["risk_level"] == "high_risk"
    assert {"9元", "彻底治愈"}.issubset(set(result["matched_terms"]))


def test_neutral_claim_is_limited_scope_low_risk_not_approval() -> None:
    """Preserves the distinction between no configured trigger and legal approval."""
    result = assess_by_rules("这是一款蓝色收纳盒。")

    assert result["risk_level"] == "low_risk"
    assert result["matched_terms"] == []
    assert "not legal approval" in result["next_action"].lower()


def test_find_matches_returns_unique_match_records() -> None:
    """Prevents duplicate matched-term records from cluttering a rule result."""
    matches = find_matches("治愈后又治愈", [(r"治愈", "reason")])

    assert matches == [{"text": "治愈", "reason": "reason"}]
