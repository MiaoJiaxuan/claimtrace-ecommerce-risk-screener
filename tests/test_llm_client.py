"""Offline tests for model-response parsing and evidence-grounding guards."""

import json
import os
from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from src.llm_client import OPENROUTER_URL, OpenRouterClient


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self.payload


def risk_card_payload(**overrides: object) -> dict:
    payload = {
        "risk_level": "evidence_needed",
        "highlighted_claim": "每月只花9元",
        "reason": "The price claim needs supporting records.",
        "source_title": "Test source",
        "source_url": "https://example.invalid/source",
        "next_action": "Verify the current offer.",
        "confidence": 0.75,
        "abstain": False,
    }
    payload.update(overrides)
    return payload


def test_successful_mocked_response_is_validated_and_returned(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Validates request wiring and response parsing using a local fake response."""
    monkeypatch.setattr("src.llm_client.load_dotenv", lambda: None)
    monkeypatch.setattr("src.llm_client.append_request_metrics", lambda _event: None)
    monkeypatch.setattr(
        os,
        "getenv",
        lambda key, default=None: {
            "OPENROUTER_API_KEY": "test-only-key",
            "OPENROUTER_MODEL": "offline/requested-model",
        }.get(key, default),
    )
    response_payload = {
        "model": "offline/returned-model",
        "choices": [
            {"message": {"content": json.dumps(risk_card_payload())}}
        ],
        "usage": {"total_tokens": 12},
    }
    post = Mock(return_value=FakeResponse(response_payload))
    monkeypatch.setattr("src.llm_client.requests.post", post)
    evidence = [
        {
            "case_id": "CASE-TEST",
            "title": "Test source",
            "case_text": "Evidence text",
            "risk_type": "price",
            "source_url": "https://example.invalid/source",
            "similarity_score": 0.55,
        }
    ]

    result = OpenRouterClient().assess("每月只花9元", evidence)

    assert result["risk_card"] == risk_card_payload()
    assert result["model"] == "offline/returned-model"
    assert result["usage"] == {"total_tokens": 12}
    post.assert_called_once()
    args, kwargs = post.call_args
    assert args == (OPENROUTER_URL,)
    assert kwargs["timeout"] == 60
    assert kwargs["json"]["model"] == "offline/requested-model"
    assert kwargs["headers"]["Authorization"] == "Bearer test-only-key"


def test_nonverbatim_highlight_is_suppressed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Prevents a paraphrase from being presented as an exact claim span."""
    monkeypatch.setattr("src.llm_client.load_dotenv", lambda: None)
    monkeypatch.setattr("src.llm_client.append_request_metrics", lambda _event: None)
    monkeypatch.setattr(
        os,
        "getenv",
        lambda key, default=None: "test-only-key" if key == "OPENROUTER_API_KEY" else default,
    )
    monkeypatch.setattr(
        "src.llm_client.requests.post",
        lambda *_args, **_kwargs: FakeResponse({
            "choices": [{"message": {"content": json.dumps(
                risk_card_payload(highlighted_claim="价格非常便宜")
            )}}]
        }),
    )
    evidence = [{
        "case_id": "CASE-TEST",
        "title": "Test source",
        "case_text": "Evidence text",
        "risk_type": "price",
        "source_url": "https://example.invalid/source",
        "similarity_score": 0.55,
    }]

    result = OpenRouterClient().assess("每月只花9元", evidence)

    assert result["risk_card"]["highlighted_claim"] == ""


def test_citation_not_in_retrieved_evidence_is_suppressed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Prevents invented sources from becoming clickable citations in the UI."""
    monkeypatch.setattr("src.llm_client.load_dotenv", lambda: None)
    monkeypatch.setattr("src.llm_client.append_request_metrics", lambda _event: None)
    monkeypatch.setattr(
        os,
        "getenv",
        lambda key, default=None: "test-only-key" if key == "OPENROUTER_API_KEY" else default,
    )
    monkeypatch.setattr(
        "src.llm_client.requests.post",
        lambda *_args, **_kwargs: FakeResponse({
            "choices": [{"message": {"content": json.dumps(
                risk_card_payload(
                    source_title="Invented source",
                    source_url="https://example.invalid/invented",
                )
            )}}]
        }),
    )
    evidence = [{
        "case_id": "CASE-TEST",
        "title": "Test source",
        "case_text": "Evidence text",
        "risk_type": "price",
        "source_url": "https://example.invalid/source",
        "similarity_score": 0.55,
    }]

    result = OpenRouterClient().assess("每月只花9元", evidence)

    assert result["risk_card"]["source_title"] is None
    assert result["risk_card"]["source_url"] is None


@pytest.mark.parametrize(
    ("content", "exception"),
    [
        ("not-json", json.JSONDecodeError),
        (json.dumps(risk_card_payload(risk_level="unknown")), ValidationError),
    ],
)
def test_invalid_model_content_raises_without_network(
    content: str,
    exception: type[Exception],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rejects malformed model output rather than passing an invalid risk card onward."""
    monkeypatch.setattr("src.llm_client.load_dotenv", lambda: None)
    monkeypatch.setattr("src.llm_client.append_request_metrics", lambda _event: None)
    monkeypatch.setattr(
        os,
        "getenv",
        lambda key, default=None: "test-only-key" if key == "OPENROUTER_API_KEY" else default,
    )
    monkeypatch.setattr(
        "src.llm_client.requests.post",
        lambda *_args, **_kwargs: FakeResponse(
            {"choices": [{"message": {"content": content}}]}
        ),
    )

    with pytest.raises(exception):
        OpenRouterClient().assess("sample claim", [])


def test_missing_api_key_fails_before_http_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ensures missing credentials fail before any HTTP request can be attempted."""
    monkeypatch.setattr("src.llm_client.load_dotenv", lambda: None)
    getenv = Mock(return_value=None)
    monkeypatch.setattr(os, "getenv", getenv)
    post = Mock(side_effect=AssertionError("HTTP must not be called"))
    monkeypatch.setattr("src.llm_client.requests.post", post)

    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        OpenRouterClient()

    post.assert_not_called()
