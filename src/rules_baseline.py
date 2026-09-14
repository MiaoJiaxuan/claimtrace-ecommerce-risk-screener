import re


HIGH_RISK_PATTERNS = [
    (
        r"(彻底治愈|治愈|根治|包治)",
        "The claim makes a medical or cure-related promise.",
    ),
    (
        r"(国家级|最高级|最佳)",
        "The claim uses a prohibited or high-risk superlative.",
    ),
]

EVIDENCE_PATTERNS = [
    (
        r"(销量|销售量|排名).{0,6}(第一|领先)",
        "The sales or ranking claim requires verifiable supporting evidence.",
    ),
    (
        r"\d+(?:\.\d+)?\s*元(?:/月|每月)?",
        "The price claim requires verification against the actual offer.",
    ),
    (
        r"(改善|提升|减少|有效|持久)",
        "The product-effect claim requires supporting evidence.",
    ),
]


def find_matches(claim: str, patterns: list[tuple[str, str]]) -> list[dict]:
    """Return all unique text spans matched by the configured patterns."""
    matches = []

    for pattern, reason in patterns:
        for match in re.finditer(pattern, claim):
            item = {
                "text": match.group(0),
                "reason": reason,
            }

            if item not in matches:
                matches.append(item)

    return matches


def assess_by_rules(claim: str) -> dict:
    """Return a rule-based assessment for one Chinese claim."""
    cleaned_claim = claim.strip()

    if not cleaned_claim:
        return {
            "risk_level": "insufficient_evidence",
            "matched_terms": [],
            "reason": "No claim was provided.",
            "next_action": "Enter a product claim for screening.",
            "method": "rules_baseline",
        }

    high_risk_matches = find_matches(
        cleaned_claim,
        HIGH_RISK_PATTERNS,
    )

    evidence_matches = find_matches(
        cleaned_claim,
        EVIDENCE_PATTERNS,
    )

    all_matches = high_risk_matches + evidence_matches
    matched_terms = list(
        dict.fromkeys(item["text"] for item in all_matches)
    )

    if high_risk_matches:
        reasons = list(
            dict.fromkeys(item["reason"] for item in all_matches)
        )

        return {
            "risk_level": "high_risk",
            "matched_terms": matched_terms,
            "reason": " ".join(reasons),
            "next_action": (
                "Do not publish the claim without revision and human review."
            ),
            "method": "rules_baseline",
        }

    if evidence_matches:
        reasons = list(
            dict.fromkeys(item["reason"] for item in evidence_matches)
        )

        return {
            "risk_level": "evidence_needed",
            "matched_terms": matched_terms,
            "reason": " ".join(reasons),
            "next_action": (
                "Verify the claim using reliable business records "
                "before publication."
            ),
            "method": "rules_baseline",
        }

    return {
        "risk_level": "low_risk",
        "matched_terms": [],
        "reason": (
            "No configured rule was triggered within the limited "
            "project scope."
        ),
        "next_action": (
            "Continue human review. This result is not legal approval."
        ),
        "method": "rules_baseline",
    }