# Evaluation guide

This directory contains the locked holdout, human reviews and evaluation scripts. Model-backed scripts can incur OpenRouter charges and load embedding weights. The table below identifies their outputs. Run experiments in an isolated copy to preserve the saved results; `pytest.ini` limits routine tests to `tests/`.

## Evidence files

| File | What it records | Interpretation |
| --- | --- | --- |
| `test_set_locked.csv` | 30 fixed test claims and project reference labels | Protected holdout: 12 `high_risk`, 13 `evidence_needed`, 5 `low_risk`. Never edit or use for tuning. |
| `retrieval_audit_10.csv` | Ten human-checked Chinese development queries | 7/10 exact expected case-ID matches; all ten were judged semantically relevant and supportive of a risk reminder. This selected sample is not a general retrieval-accuracy estimate. |
| `manual_review_20.xlsx` | Twenty completed human reviews, split evenly between case-derived and synthetic samples | Retains reviewer conclusions and structured checks; see `../results/manual_review_summary.csv` for counts. Recommendation actionability was not assessable from missing historical `next_action` values. |
| `../results/test_baseline.csv`, `test_full.csv`, `test_summary.csv`, `test_metrics.csv` | Saved historical locked-set outputs and summaries | The saved evaluation predates the current response guards. |
| `../results/dev_retrieval.csv` | Saved development retrieval output | Reuse for documented analyses; do not rerun retrieval just to reproduce the audit unless model/environment details and output destination are controlled. |

## Script inventory and side effects

| Script | Main operation | Writes / external action |
| --- | --- | --- |
| `baseline_dev.py` | Run keyword rules on development claims | Writes `results/dev_baseline.csv`. |
| `baseline_test.py` | Run keyword rules on the locked test set | Writes `results/test_baseline.csv`; do not overwrite the saved result casually. |
| `summarize_dev.py`, `summarize_test.py` | Summarise saved result files | Write summary CSVs under `results/`. |
| `compare_test.py` | Join and compare saved test outputs by `claim_id` | Writes `results/test_comparison.csv`. |
| `metrics_test.py` | Validate saved test IDs/labels and compute metrics | Writes `results/test_metrics.csv`; it does not call a model. |
| `evaluate.py` | Run retrieval on development claims | Constructs the embedding model (may require a model download) and writes `results/dev_retrieval.csv`. |
| `pilot.py` | Assess five selected development claims | Calls the configured model when retrieval passes threshold; writes `results/dev_pilot.csv`; may incur API cost. |
| `full_dev.py` | Run/resume the full development assessment | Calls the configured model for pending rows and appends to `results/dev_full.csv`; may incur API cost. |
| `test_full.py` | Run/resume the locked-test assessment | Calls the configured model and appends to `results/test_full.csv`; can incur cost and alter the saved formal result. Do not run as a routine check. |
| `lock_test.py` | Create the locked test CSV if it does not already exist | Writes `test_set_locked.csv`; never run to replace or reconstruct an existing locked set. |

## What the reported metrics mean

The baseline and ClaimTrace use the same 30 saved IDs and project reference labels. For the original combined positive class (`high_risk` plus `evidence_needed`), there are 25 positives; the saved ClaimTrace result detects 17, giving recall 17/25 = 68%, below the proposal's 80% target. `insufficient_evidence` is a human-review abstention, not an automatic detection. For the separate `high_risk` class there are 12 positives; ClaimTrace recall is 10/12 = 83.3%, with precision 10/17 = 58.8%. The two positive-class definitions are reported separately.

Three-class Macro F1 is the unweighted average of F1 for the three project labels; the saved values are 40.5% for the rule baseline and 48.0% for ClaimTrace. ClaimTrace predicted no `evidence_needed` labels. Coverage is 20/30 = 66.7%; abstention/human-review prompt rate is 10/30 = 33.3%; judged-item label agreement is 13/20 = 65.0%. The seller arranges human review when requested.

For the 20 completed human reviews, citation support is 10/11 = 90.9% among records with a citation marked present and assessable. Nine reviewed records have no applicable citation. See the [evidence tables](../docs/EVALUATION_EVIDENCE_EN.md) and [product documentation](../docs/PRODUCT_DOCUMENTATION_EN.md) for sources, labels and denominators.

## Re-running safely

Use an isolated copy for scripts that write to `results/`. Select model or threshold changes on development data, then evaluate a new holdout. Preserve the original locked labels and predictions for comparison. Routine unit tests use fixed mocks and make no OpenRouter requests.
