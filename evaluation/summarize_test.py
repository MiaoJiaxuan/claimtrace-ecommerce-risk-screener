"""Summarise saved locked-test outputs and write results/test_summary.csv."""

from pathlib import Path

import pandas as pd


data = pd.read_csv("results/test_full.csv")

if len(data) != 30 or data["claim_id"].duplicated().any():
    raise ValueError("Expected 60 unique development results")

# 明确识别 True/False，避免把“转人工”误算成分类结果。
data["abstained_bool"] = (
    data["abstained"].astype(str).str.lower().eq("true")
)

rows = []

for name, group in [
    ("case_derived", data[data["source_type"] == "case_derived"]),
    ("synthetic", data[data["source_type"] == "synthetic"]),
    ("all", data),
]:
    classified = group[~group["abstained_bool"]]
    matches = (
        classified["expected_label"] == classified["predicted_label"]
    ).sum()

    rows.append({
        "group": name,
        "total": len(group),
        "classified": len(classified),
        "abstained": int(group["abstained_bool"].sum()),
        "matched_classified": int(matches),
        "match_rate_classified_pct": round(
            100 * matches / len(classified), 1
        ) if len(classified) else 0,
        "coverage_pct": round(
            100 * len(classified) / len(group), 1
        )
    })

summary = pd.DataFrame(rows)
output = Path("results/test_summary.csv")
summary.to_csv(output, index=False, encoding="utf-8-sig")

print(summary.to_string(index=False))
print(f"Saved: {output}")
