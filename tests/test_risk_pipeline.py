"""Test pipeline abstention and dispatch boundaries with mocked dependencies."""

from unittest.mock import Mock

import pytest

import src.risk_pipeline as risk_pipeline


def retrieved_case(score: float) -> dict:
    return {
        "case_id": "CASE-TEST",
        "title": "Test case",
        "case_text": "Test evidence",
        "risk_type": "evidence_needed",
        "source_url": "https://example.invalid/case",
        "similarity_score": score,
    }


class FakeRetriever:
    def __init__(self, cases: list[dict]) -> None:
        self.cases = cases
        self.retrieve = Mock(return_value=cases)


class FakeLLM:
    def __init__(self, result: dict) -> None:
        self.result = result
        self.assess = Mock(return_value=result)


def install_fakes(
    monkeypatch: pytest.MonkeyPatch,
    cases: list[dict],
    llm_result: dict | None = None,
) -> tuple[FakeRetriever, FakeLLM]:
    retriever = FakeRetriever(cases)
    llm = FakeLLM(
        llm_result
        or {
            "risk_card": {"risk_level": "evidence_needed"},
            "model": "offline/fake",
            "usage": {},
        }
    )
    monkeypatch.setattr(risk_pipeline, "CaseRetriever", lambda: retriever)
    monkeypatch.setattr(risk_pipeline, "OpenRouterClient", lambda: llm)
    return retriever, llm


def test_score_below_030_abstains_without_constructing_or_calling_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Enforces abstention strictly below 0.30 and forbids model construction."""
    retriever, _ = install_fakes(monkeypatch, [retrieved_case(0.2999)])
    model_constructions = Mock(side_effect=AssertionError("model must not be used"))
    monkeypatch.setattr(risk_pipeline, "OpenRouterClient", model_constructions)

    result = risk_pipeline.ClaimTracePipeline().assess("sample claim")

    assert result["llm_called"] is False
    assert result["risk_card"]["risk_level"] == "insufficient_evidence"
    assert result["risk_card"]["abstain"] is True
    assert result["retrieval"]["top_score"] == 0.2999
    assert result["retrieval"]["threshold"] == 0.30
    assert retriever.retrieve.call_count == 1
    model_constructions.assert_not_called()


@pytest.mark.parametrize("score", [0.30, 0.45])
def test_score_at_or_above_030_calls_mock_model_once(
    score: float,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Protects the inclusive >= 0.30 gate and one-call maximum above threshold."""
    retriever, llm = install_fakes(monkeypatch, [retrieved_case(score)])

    result = risk_pipeline.ClaimTracePipeline().assess("sample claim")

    assert result["llm_called"] is True
    assert result["risk_card"]["risk_level"] == "evidence_needed"
    assert result["model"] == "offline/fake"
    assert retriever.retrieve.call_count == 1
    llm.assess.assert_called_once_with("sample claim", [retrieved_case(score)])


def test_no_retrieved_cases_abstains_without_model_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Routes missing retrieval evidence to a human without invoking the model."""
    _, _ = install_fakes(monkeypatch, [])
    model_constructions = Mock(side_effect=AssertionError("model must not be used"))
    monkeypatch.setattr(risk_pipeline, "OpenRouterClient", model_constructions)

    result = risk_pipeline.ClaimTracePipeline().assess("sample claim")

    assert result["llm_called"] is False
    assert result["retrieval"]["top_score"] == 0.0
    assert result["risk_card"]["risk_level"] == "insufficient_evidence"
    model_constructions.assert_not_called()
