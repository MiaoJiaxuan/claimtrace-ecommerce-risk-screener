"""Run the locked-test rule baseline; writes results/test_baseline.csv."""

from pathlib import Path
import pandas as pd
from src.rules_baseline import assess_by_rules

test = pd.read_csv("evaluation/test_set_locked.csv")

if len(test) != 30 or test["claim_id"].duplicated().any():
    raise ValueError("锁定测试集应有 30 条，且编号不能重复")

rows = []
for claim in test.itertuples(index=False):
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
output.to_csv("results/test_baseline.csv", index=False, encoding="utf-8-sig")

matches = (output["expected_label"] == output["predicted_label"]).sum()
print(f"Test claims: {len(output)}")
print(f"Exact matches: {matches}/30")
print(pd.crosstab(
    [output["source_type"], output["expected_label"]],
    output["predicted_label"],
))
print("Saved: results/test_baseline.csv")
