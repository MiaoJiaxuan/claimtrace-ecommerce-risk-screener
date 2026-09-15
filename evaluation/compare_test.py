import pandas as pd

trace = pd.read_csv("results/test_full.csv")
baseline = pd.read_csv("results/test_baseline.csv")

if len(trace) != 30 or len(baseline) != 30:
    raise ValueError("两份测试结果都应有 30 条")

baseline = baseline[["claim_id", "predicted_label"]].rename(
    columns={"predicted_label": "baseline_label"}
)
comparison = trace.merge(baseline, on="claim_id", validate="one_to_one")

abstained = comparison["abstained"].astype(str).str.lower().eq("true")

comparison["baseline_status"] = "mismatch"
comparison.loc[
    comparison["baseline_label"] == comparison["expected_label"],
    "baseline_status"
] = "match"

comparison["trace_status"] = "mismatch"
comparison.loc[
    comparison["predicted_label"] == comparison["expected_label"],
    "trace_status"
] = "match"
comparison.loc[abstained, "trace_status"] = "human_review"

columns = [
    "claim_id", "claim_zh", "source_type", "expected_label",
    "baseline_label", "baseline_status", "predicted_label",
    "trace_status", "top_score", "reason",
]
comparison[columns].to_csv(
    "results/test_comparison.csv", index=False, encoding="utf-8-sig"
)

print(pd.crosstab(
    comparison["source_type"], comparison["trace_status"]
))
print("Saved: results/test_comparison.csv")