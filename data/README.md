# Data inventory

This directory contains the project claim samples, example inputs, label guide and case records used by ClaimTrace. The data are project assets for a course prototype; do not interpret project labels as official regulator findings.

| File | Role | Scope and handling |
| --- | --- | --- |
| `claims.csv` | Claim-level development and test samples | 90 Chinese claims with project reference labels and English translations; 45 `case_derived` and 45 `synthetic`. The project split uses 60 development and 30 test records. The locked test copy is stored separately at `../evaluation/test_set_locked.csv`. |
| `examples.csv` | UI sample claims | Ten examples available for demonstrating input behavior. They are examples, not a representative sample of sellers or marketplace traffic. |
| `label_guide.md` | Project reference-label definitions | Defines `high_risk`, `evidence_needed` and `low_risk` for this evaluation. They are project labels, not official legal or regulatory categories. |
| `sources.csv` | Retrieved public enforcement-case records | Contains case identifiers, publisher/date metadata, title, a case-text summary, risk type and source URL. These records support retrieval and contextual reminders; a similar case does not prove a new seller made the same claim or committed a violation. |

## Sample construction and limits

`case_derived` items are rewritten from existing case material; `synthetic` items are constructed examples. The repository does not contain a verified generation script or complete prompt history for reproducing every item. The samples are not a random draw from real product listings, and the 30-item locked set is too small to establish population-level performance.

The author read the linked public sources and wrote the case summaries. Each record retains its publisher, publication date, title and URL so readers can consult the original facts. The summaries are project-authored; they do not transfer the original publishers' rights or imply a blanket licence for third-party material. External pages may change or become unavailable.

## Label and test-set protection

Use `data/label_guide.md` when interpreting labels. Keep the reference labels separate from system outputs. `evaluation/test_set_locked.csv` is a fixed holdout and must not be edited or used to tune rules, prompts, models or thresholds. The current test distribution is 12 `high_risk`, 13 `evidence_needed` and 5 `low_risk` items; see the evaluation guide for the saved result files and denominators.
