from pathlib import Path

import pandas as pd

from src.risk_pipeline import ClaimTracePipeline


PILOT_IDS = [
    "CLAIM001",  # 需要证据
    "CLAIM002",  # 高风险
    "CLAIM046",  # 普通商品描述，但检索分数超过阈值
    "CLAIM064",  # 高风险，但检索证据不足
    "CLAIM071",  # 需要证据，但检索证据不足
]

claims = pd.read_csv("data/claims.csv")
pilot = claims[claims["claim_id"].isin(PILOT_IDS)]

if len(pilot) != 5 or set(pilot["split"]) != {"development"}:
    raise ValueError("Pilot claims must be five development records")

pipeline = ClaimTracePipeline()
rows = []

for claim in pilot.itertuples(index=False):
    result = pipeline.assess(claim.claim_zh)
    prediction = result["risk_card"]["risk_level"]

    rows.append({
        "claim_id": claim.claim_id,
        "claim_zh": claim.claim_zh,
        "expected_label": claim.label,
        "predicted_label": prediction,
        "top_score": result["retrieval"]["top_score"],
        "llm_called": result["llm_called"],
    })

    print(f"{claim.claim_id}: {claim.label} -> {prediction}")

Path("results").mkdir(exist_ok=True)
pd.DataFrame(rows).to_csv(
    "results/dev_pilot.csv",
    index=False,
    encoding="utf-8-sig",
)

print("Saved: results/dev_pilot.csv")