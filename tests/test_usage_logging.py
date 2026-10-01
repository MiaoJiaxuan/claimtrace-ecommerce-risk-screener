"""Test privacy-minimised request metric construction and append behavior."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

from src.llm_client import OpenRouterClient


SENSITIVE_CLAIM = "这是一条不应写入日志的完整中文商品文案。"
SENSITIVE_URL = "https://example.invalid/private-case"


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self.payload


def risk_card_payload() -> dict:
    return {
        "risk_level": "evidence_needed",
        "highlighted_claim": "这是一条",
        "reason": "Supporting records are needed.",
        "source_title": "Example case",
        "source_url": SENSITIVE_URL,
        "next_action": "Request supporting records.",
        "confidence": 0.72,
        "abstain": False,
    }


def retrieved_cases() -> list[dict]:
    return [
        {
            "case_id": "CASE_TEST",
            "title": "Example case",
            "case_text": "Private evidence text that must not be logged.",
            "risk_type": "evidence_needed",
            "source_url": SENSITIVE_URL,
            "similarity_score": 0.55,
        }
    ]


def read_events(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]


class UsageLoggingTests(unittest.TestCase):
    def setUp(self) -> None:
        """Keep every mocked request test from reading a real .env file."""
        dotenv_patch = patch("src.llm_client.load_dotenv", return_value=None)
        dotenv_patch.start()
        self.addCleanup(dotenv_patch.stop)

    def test_successful_request_logs_provider_usage_without_content(self) -> None:
        """Protects privacy while recording real response usage from a mock."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            log_path = Path(temporary_directory) / "request_metrics.jsonl"
            response_payload = {
                "model": "test/returned-model",
                "choices": [
                    {"message": {"content": json.dumps(risk_card_payload())}}
                ],
                "usage": {
                    "prompt_tokens": 120,
                    "completion_tokens": 45,
                    "total_tokens": 165,
                    "cost": 0.00123,
                },
            }
            environment = {
                "OPENROUTER_API_KEY": "test-secret-key",
                "OPENROUTER_MODEL": "test/requested-model",
                "CLAIMTRACE_METRICS_LOG_PATH": str(log_path),
            }
            with (
                patch.dict(os.environ, environment, clear=False),
                patch(
                    "src.llm_client.requests.post",
                    return_value=FakeResponse(response_payload),
                ),
            ):
                result = OpenRouterClient().assess(
                    SENSITIVE_CLAIM,
                    retrieved_cases(),
                )

            self.assertEqual(
                result,
                {
                    "risk_card": risk_card_payload(),
                    "model": "test/returned-model",
                    "usage": response_payload["usage"],
                },
            )
            event = read_events(log_path)[0]
            self.assertEqual(event["model_requested"], "test/requested-model")
            self.assertEqual(event["model_returned"], "test/returned-model")
            self.assertEqual(event["prompt_tokens"], 120)
            self.assertEqual(event["completion_tokens"], 45)
            self.assertEqual(event["total_tokens"], 165)
            self.assertEqual(event["provider_cost_usd"], 0.00123)
            self.assertIsNone(event["estimated_cost_usd"])
            self.assertIsNone(event["pricing_source"])
            self.assertIsNone(event["pricing_date"])
            self.assertEqual(event["request_status"], "success")
            self.assertIsNone(event["error_type"])
            self.assertGreaterEqual(event["latency_seconds"], 0)
            self.assertTrue(event["request_id"])
            self.assertTrue(event["timestamp_utc"].endswith("Z"))

            serialized = json.dumps(event, ensure_ascii=False)
            self.assertNotIn(SENSITIVE_CLAIM, serialized)
            self.assertNotIn(SENSITIVE_URL, serialized)
            self.assertNotIn("test-secret-key", serialized)
            self.assertNotIn("Private evidence text", serialized)

    def test_missing_usage_is_logged_as_null_not_zero(self) -> None:
        """Keeps absent provider measurements distinct from measured zero values."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            log_path = Path(temporary_directory) / "request_metrics.jsonl"
            response_payload = {
                "model": "test/model",
                "choices": [
                    {"message": {"content": json.dumps(risk_card_payload())}}
                ],
            }
            environment = {
                "OPENROUTER_API_KEY": "test-key",
                "CLAIMTRACE_METRICS_LOG_PATH": str(log_path),
            }
            with (
                patch.dict(os.environ, environment, clear=False),
                patch(
                    "src.llm_client.requests.post",
                    return_value=FakeResponse(response_payload),
                ),
            ):
                OpenRouterClient().assess(SENSITIVE_CLAIM, retrieved_cases())

            event = read_events(log_path)[0]
            for field in [
                "prompt_tokens",
                "completion_tokens",
                "total_tokens",
                "provider_cost_usd",
            ]:
                self.assertIsNone(event[field])

    def test_failed_request_logs_only_error_type_and_reraises(self) -> None:
        """Preserves request failure behavior without logging sensitive content."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            log_path = Path(temporary_directory) / "request_metrics.jsonl"
            environment = {
                "OPENROUTER_API_KEY": "test-key",
                "CLAIMTRACE_METRICS_LOG_PATH": str(log_path),
            }
            with (
                patch.dict(os.environ, environment, clear=False),
                patch(
                    "src.llm_client.requests.post",
                    side_effect=requests.Timeout("sensitive error detail"),
                ),
            ):
                with self.assertRaisesRegex(
                    requests.Timeout,
                    "sensitive error detail",
                ):
                    OpenRouterClient().assess(
                        SENSITIVE_CLAIM,
                        retrieved_cases(),
                    )

            event = read_events(log_path)[0]
            self.assertEqual(event["request_status"], "error")
            self.assertEqual(event["error_type"], "Timeout")
            self.assertIsNone(event["model_returned"])
            self.assertIsNone(event["prompt_tokens"])
            serialized = json.dumps(event, ensure_ascii=False)
            self.assertNotIn("sensitive error detail", serialized)
            self.assertNotIn(SENSITIVE_CLAIM, serialized)

    def test_logging_failure_does_not_change_successful_assessment(self) -> None:
        """Ensures observational logging failures cannot change the assessment result."""
        response_payload = {
            "model": "test/model",
            "choices": [
                {"message": {"content": json.dumps(risk_card_payload())}}
            ],
            "usage": {"total_tokens": 10},
        }
        environment = {"OPENROUTER_API_KEY": "test-key"}
        with (
            patch.dict(os.environ, environment, clear=False),
            patch(
                "src.llm_client.requests.post",
                return_value=FakeResponse(response_payload),
            ),
            patch(
                "src.llm_client.append_request_metrics",
                side_effect=OSError("disk unavailable"),
            ),
        ):
            result = OpenRouterClient().assess(
                SENSITIVE_CLAIM,
                retrieved_cases(),
            )

        self.assertEqual(result["model"], "test/model")
        self.assertEqual(result["usage"], {"total_tokens": 10})


if __name__ == "__main__":
    unittest.main()
