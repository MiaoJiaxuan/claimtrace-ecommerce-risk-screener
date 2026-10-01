"""Create the fixed test copy only when absent; never rebuild an existing holdout."""

from pathlib import Path
import pandas as pd

claims = pd.read_csv("data/claims.csv")
test = claims[claims["split"] == "test"].copy()

if len(test) != 30 or test["claim_id"].duplicated().any():
    raise ValueError("测试集应有 30 条，且编号不能重复")

output = Path("evaluation/test_set_locked.csv")
if output.exists() and output.stat().st_size > 0:
    raise ValueError("锁定文件已有内容，请勿覆盖")

test.to_csv(output, index=False, encoding="utf-8-sig")
print(f"Locked test claims: {len(test)}")
print(f"Saved: {output}")
