# Saved results inventory

The CSV files in this directory are saved development, locked-test and human-review artifacts. They are historical outputs: later UI, validation and logging changes did not regenerate them. Do not run scripts that write into this directory as a routine verification step; the safe offline test command targets only `tests/`.

| Files | Status and use |
| --- | --- |
| `dev_baseline.csv`, `dev_full.csv`, `dev_pilot.csv`, `dev_retrieval.csv`, `dev_summary.csv` | Saved development-stage outputs; not the locked-test estimate. |
| `test_baseline.csv`, `test_full.csv` | The rule baseline and ClaimTrace predictions on the same 30 locked-test claim IDs. These are the primary row-level metric sources. |
| `test_comparison.csv`, `test_metrics.csv`, `test_summary.csv` | Saved comparison, per-class metrics and grouped summaries derived from the locked-test outputs. |
| `manual_review_summary.csv` | Structured counts from 20 completed human reviews; citation support is 10/11 among assessable, present citations, not among every request. |

The project reference labels and frozen holdout are described in [`evaluation/README.md`](../evaluation/README.md). In particular, the original combined-positive recall is 17/25 = 68%, below the proposal's 80% target; abstentions do not count as automatic detections. `insufficient_evidence` is an abstention output, not a fourth reference label.
