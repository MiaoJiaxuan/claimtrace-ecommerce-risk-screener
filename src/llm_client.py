"""Send one structured claim assessment to OpenRouter and ground citations."""

import json
import os
from time import perf_counter

import requests
from dotenv import load_dotenv

from src.schemas import RiskCard
from src.usage_logging import append_request_metrics, make_request_metrics


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _ground_response_fields(
    payload: dict,
    claim: str,
    retrieved_cases: list[dict],
) -> dict:
    """Suppress a highlighted span or citation not grounded in supplied data."""
    grounded = dict(payload)
    highlighted_claim = grounded.get("highlighted_claim", "")
    if highlighted_claim and highlighted_claim not in claim:
        grounded["highlighted_claim"] = ""

    source_title = grounded.get("source_title")
    source_url = grounded.get("source_url")
    source_is_retrieved = bool(source_title and source_url) and any(
        case.get("title") == source_title
        and case.get("source_url") == source_url
        for case in retrieved_cases
    )
    if not source_is_retrieved:
        grounded["source_title"] = None
        grounded["source_url"] = None
    return grounded


class OpenRouterClient:
    """Call one OpenRouter model for one structured assessment."""

    def __init__(self) -> None:
        load_dotenv()

        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "openai/gpt-4o-mini",
        )

        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY was not found in the .env file."
            )

    def assess(
        self,
        claim: str,
        retrieved_cases: list[dict],
    ) -> dict:
        """Assess one claim using only the supplied evidence."""
        evidence_text = "\n\n".join(
            (
                f"Case ID: {case['case_id']}\n"
                f"Title: {case['title']}\n"
                f"Case summary: {case['case_text']}\n"
                f"Risk type: {case['risk_type']}\n"
                f"Source URL: {case['source_url']}\n"
                f"Similarity score: {case['similarity_score']}"
            )
            for case in retrieved_cases
        )

        system_prompt = """
You assess Chinese e-commerce advertising claims for preliminary screening.

Use only the submitted claim and retrieved enforcement-case evidence.
Do not provide final legal advice.
Do not invent laws, cases, facts or source URLs.

Return one JSON object with exactly these fields:
risk_level, highlighted_claim, reason, source_title, source_url,
next_action, confidence, abstain.

Allowed risk levels:
high_risk, evidence_needed, low_risk, insufficient_evidence.

Use high_risk for a strong cure promise or a clearly prohibited expression.

A retrieved enforcement case proves what happened in that specific case.
Similar wording alone does not prove the submitted product or seller made
the same false claim. Do not transfer factual findings from one seller to
another.

Use evidence_needed for price, quantity, ranking, rating, or performance
claims that require reliable supporting records, unless the supplied
evidence establishes that this is the same product and seller.

Use low_risk only when no configured concern is identified. Clearly state
that this is not legal approval.

Use insufficient_evidence and abstain=true when the supplied evidence does
not support a reliable assessment.

highlighted_claim must be copied verbatim from the submitted claim as one
contiguous substring. If no exact span can be identified, return an empty
string. Never paraphrase the highlighted span.

Write reason and next_action in clear English.
Copy source_title and source_url together from the same supplied evidence
record. If no supplied record is cited, return null for both fields.
confidence must be a JSON number between 0 and 1, such as 0.85, and must not be a word such as high, medium or low.
Return JSON only.
""".strip()

        user_prompt = (
            f"Submitted Chinese claim:\n{claim}\n\n"
            f"Retrieved evidence:\n{evidence_text}"
        )

        request_started = perf_counter()
        response_data = None

        try:
            response = requests.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "temperature": 0,
                   "provider": {
    "require_parameters": True,
},
"response_format": {
    "type": "json_schema",
    "json_schema": {
        "name": "risk_card",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "risk_level": {
                    "type": "string",
                    "enum": [
                        "high_risk",
                        "evidence_needed",
                        "low_risk",
                        "insufficient_evidence",
                    ],
                },
                "highlighted_claim": {
                    "type": "string",
                },
                "reason": {
                    "type": "string",
                },
                "source_title": {
                    "type": ["string", "null"],
                },
                "source_url": {
                    "type": ["string", "null"],
                },
                "next_action": {
                    "type": "string",
                },
                "confidence": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                },
                "abstain": {
                    "type": "boolean",
                },
            },
            "required": [
                "risk_level",
                "highlighted_claim",
                "reason",
                "source_title",
                "source_url",
                "next_action",
                "confidence",
                "abstain",
            ],
            "additionalProperties": False,
        },
    },
},
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],
                },
                timeout=60,
            )

            response.raise_for_status()
            response_data = response.json()

            content = response_data["choices"][0]["message"]["content"]
            parsed_content = json.loads(content)

            grounded_content = _ground_response_fields(
                parsed_content,
                claim,
                retrieved_cases,
            )
            risk_card = RiskCard.model_validate(grounded_content)
        except Exception as error:
            self._record_request_metrics(
                response_data=response_data,
                latency_seconds=perf_counter() - request_started,
                request_status="error",
                error_type=type(error).__name__,
            )
            raise

        self._record_request_metrics(
            response_data=response_data,
            latency_seconds=perf_counter() - request_started,
            request_status="success",
            error_type=None,
        )

        return {
            "risk_card": risk_card.model_dump(),
            "model": response_data.get("model", self.model),
            "usage": response_data.get("usage", {}),
        }

    def _record_request_metrics(
        self,
        *,
        response_data: object,
        latency_seconds: float,
        request_status: str,
        error_type: str | None,
    ) -> None:
        """Best-effort logging that cannot change an assessment outcome."""
        try:
            response_metadata = (
                response_data if isinstance(response_data, dict) else {}
            )
            event = make_request_metrics(
                model_requested=self.model,
                model_returned=response_metadata.get("model"),
                usage=response_metadata.get("usage"),
                latency_seconds=latency_seconds,
                request_status=request_status,
                error_type=error_type,
            )
            append_request_metrics(event)
        except Exception:
            # Metrics are observational and must never alter user-facing logic.
            pass
