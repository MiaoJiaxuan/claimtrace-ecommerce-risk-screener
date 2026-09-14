import re


HIGH_RISK_TERMS = {
    "国家级": "The claim uses a national-level superlative.",
    "最高级": "The claim uses a highest-level superlative.",
    "最佳": "The claim uses a best-ranking superlative.",
}


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


def assess_by_rules(claim: str) -> dict:
    """Return a simple rule-based assessment for one Chinese claim."""

    cleaned_claim = claim.strip()

    if not cleaned_claim:
        return {
            "risk_level": "insufficient_evidence",
            "matched_terms": [],
            "reason": "No claim was provided.",
            "next_action": "Enter a product claim for screening.",
            "method": "rules_baseline",
        }

    high_risk_matches = [
        term for term in HIGH_RISK_TERMS if term in cleaned_claim
    ]

    if high_risk_matches:
        return {
            "risk_level": "high_risk",
            "matched_terms": high_risk_matches,
            "reason": HIGH_RISK_TERMS[high_risk_matches[0]],
            "next_action": (
                "Remove or revise the highlighted superlative "
                "and obtain human review."
            ),
            "method": "rules_baseline",
        }

    evidence_matches = []

    for pattern, reason in EVIDENCE_PATTERNS:
        if re.search(pattern, cleaned_claim):
            evidence_matches.append((pattern, reason))

    if evidence_matches:
        return {
            "risk_level": "evidence_needed",
            "matched_terms": [
                match.group(0)
                for pattern, _ in evidence_matches
                if (match := re.search(pattern, cleaned_claim))
            ],
            "reason": evidence_matches[0][1],
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