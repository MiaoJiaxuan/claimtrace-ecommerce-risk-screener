"""Run development-set rule baseline and write results/dev_baseline.csv."""

from pathlib import Path

import pandas as pd

from src.rules_baseline import assess_by_rules

claims = pd.read_csv("data/claims.csv")
dev = claims[claims["split"] == "development"]

if len(dev) != 60 or dev["claim_id"].duplicated().any():
    raise ValueError("开发集应有 60 条，且 claim_id 不能重复")

rows = []
for claim in dev.itertuples(index=False):
    result = assess_by_rules(claim.claim_zh)
    rows.append({
        "claim_id": claim.claim_id,
        "claim_zh": claim.claim_zh,
        "expected_label": claim.label,
        "source_type": claim.source_type,
        "predicted_label": result["risk_level"],
        "matched_terms": "；".join(result["matched_terms"]),
        "reason": result["reason"],
    })

output = pd.DataFrame(rows)
Path("results").mkdir(exist_ok=True)
output.to_csv("results/dev_baseline.csv", index=False, encoding="utf-8-sig")

matches = (output["expected_label"] == output["predicted_label"]).sum()
print(f"Development claims: {len(output)}")
print(f"Exact matches: {matches}/60")
print(pd.crosstab(
    [output["source_type"], output["expected_label"]],
    output["predicted_label"],
))
print("Saved: results/dev_baseline.csv")
