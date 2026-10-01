"""Run or resume model-backed development assessments and append result rows."""

from pathlib import Path

import pandas as pd

from src.risk_pipeline import ClaimTracePipeline


OUTPUT = Path("results/dev_full.csv")

claims = pd.read_csv("data/claims.csv")
development = claims[claims["split"] == "development"]

if len(development) != 60:
    raise ValueError(f"Expected 60 development claims, found {len(development)}")

OUTPUT.parent.mkdir(exist_ok=True)

# 如果中途停止，再运行时跳过已经保存的文案。
done = set()
if OUTPUT.exists():
    done = set(pd.read_csv(OUTPUT)["claim_id"])

pipeline = ClaimTracePipeline()

for claim in development.itertuples(index=False):
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
        OUTPUT,
        mode="a",
        header=not OUTPUT.exists(),
        index=False,
        encoding="utf-8",
    )
    print(f"Saved {claim.claim_id}: {card['risk_level']}")

final = pd.read_csv(OUTPUT)
print(f"Completed: {len(final)}/60")
print(f"Results saved: {OUTPUT}")
