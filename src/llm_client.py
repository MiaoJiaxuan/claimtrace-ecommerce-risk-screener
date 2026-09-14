import json
import os

import requests
from dotenv import load_dotenv

from src.schemas import RiskCard


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


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

Use high_risk for a strong cure promise, prohibited superlative or a claim
that closely matches a serious confirmed enforcement pattern.

Use evidence_needed when the claim requires reliable supporting records.

Use low_risk only when no configured concern is identified. Clearly state
that this is not legal approval.

Use insufficient_evidence and abstain=true when the supplied evidence does
not support a reliable assessment.

Write reason and next_action in clear English.
Copy source_title and source_url only from the supplied evidence.
confidence must be a JSON number between 0 and 1, such as 0.85, and must not be a word such as high, medium or low.
Return JSON only.
""".strip()

        user_prompt = (
            f"Submitted Chinese claim:\n{claim}\n\n"
            f"Retrieved evidence:\n{evidence_text}"
        )

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

        risk_card = RiskCard.model_validate(parsed_content)

        return {
            "risk_card": risk_card.model_dump(),
            "model": response_data.get("model", self.model),
            "usage": response_data.get("usage", {}),
        }