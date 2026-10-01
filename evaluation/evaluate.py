"""Run development retrieval; may load/download an embedding model and write CSV."""

from pathlib import Path

import pandas as pd

from src.risk_pipeline import ClaimTracePipeline


claims = pd.read_csv("data/claims.csv")
development = claims[claims["split"] == "development"]

if len(development) != 60:
    raise ValueError(f"Expected 60 development claims, found {len(development)}")

pipeline = ClaimTracePipeline()
rows = []

for claim in development.itertuples(index=False):
    result = pipeline.retrieve_evidence(claim.claim_zh)
    cases = result["retrieved_cases"]

    rows.append({
        "claim_id": claim.claim_id,
        "expected_label": claim.label,
        "source_type": claim.source_type,
        "related_case_id": claim.related_case_id,
        "top_case_id": cases[0]["case_id"] if cases else "",
        "top_score": result["top_score"],
        "abstained": result["abstain"],
    })

output = pd.DataFrame(rows)
Path("results").mkdir(exist_ok=True)
output.to_csv("results/dev_retrieval.csv", index=False, encoding="utf-8-sig")

print("Development claims:", len(output))
print("Abstained:", int(output["abstained"].sum()))
print("Results saved: results/dev_retrieval.csv")
print("\nAbstention by reference label:")
print(output.groupby("expected_label")["abstained"].agg(["sum", "count"]))
