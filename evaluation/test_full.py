"""Run/resume model-backed locked-test scoring; may cost money and writes results."""

from pathlib import Path
import pandas as pd
from src.risk_pipeline import ClaimTracePipeline

OUTPUT = Path("results/test_full.csv")
test = pd.read_csv("evaluation/test_set_locked.csv")

if len(test) != 30 or test["claim_id"].duplicated().any():
    raise ValueError("The locked test set must contain 30 unique claim IDs")

OUTPUT.parent.mkdir(exist_ok=True)

# Resume without repeating claims already saved before an interruption.
done = set()
if OUTPUT.exists() and OUTPUT.stat().st_size > 0:
    done = set(pd.read_csv(OUTPUT)["claim_id"])

pipeline = ClaimTracePipeline()

for claim in test.itertuples(index=False):
    if claim.claim_id in done:
        continue

    result = pipeline.assess(claim.claim_zh)
    card = result["risk_card"]

    row = {
        "claim_id": claim.claim_id,
        "claim_zh": claim.claim_zh,
        "expected_label": claim.label,
        "source_type": claim.source_type,
        "predicted_label": card["risk_level"],
        "abstained": card["abstain"],
        "top_score": result["retrieval"]["top_score"],
        "llm_called": result["llm_called"],
        "reason": card["reason"],
        "source_title": card["source_title"],
        "source_url": card["source_url"],
    }

    pd.DataFrame([row]).to_csv(
        OUTPUT, mode="a", header=not OUTPUT.exists(),
        index=False, encoding="utf-8",
    )
    print(f"Saved {claim.claim_id}: {card['risk_level']}")

final = pd.read_csv(OUTPUT)
print(f"Completed: {len(final)}/30")
print(f"Results saved: {OUTPUT}")
