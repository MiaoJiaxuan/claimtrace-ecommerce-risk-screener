# Evaluation evidence and denominators

This guide links reported numbers to saved evidence. It does not describe a new model run. Reference labels and the locked holdout remain unchanged; later UI and response-guard improvements are not retroactively attributed to these results.

## Locked sample and system comparison

The [locked set](../evaluation/test_set_locked.csv) contains 30 unique claim IDs: 12 `high_risk`, 13 `evidence_needed`, five `low_risk`; 15 case-derived and 15 synthetic. The [baseline](../results/test_baseline.csv) and [ClaimTrace](../results/test_full.csv) use those same IDs and reference labels. The 80% target applies to the combined positive class, not the high-risk-only class.

| Positive definition | System | TP | FP | FN | Precision | Recall | F1 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| High risk | Baseline | 3 | 0 | 9 | 3/3 = 100% | 3/12 = 25% | 40.0% |
| High risk | ClaimTrace | 10 | 7 | 2 | 10/17 = 58.8% | 10/12 = 83.3% | 69.0% |
| High risk + evidence needed | Baseline | 8 | 0 | 17 | 8/8 = 100% | 8/25 = 32% | 48.5% |
| High risk + evidence needed | ClaimTrace | 17 | 0 | 8 | 17/17 = 100% | 17/25 = 68% | 81.0% |

Combined predictions count only `high_risk` or `evidence_needed` as automatically detected. A positive example returned as `insufficient_evidence` remains a false negative. Combined figures are calculated from the two saved prediction files; they are not a change to the per-class [saved metric table](../results/test_metrics.csv).

## Coverage and agreement

| System or ClaimTrace group | Total | Assessed | Abstained | Agreement among assessed | Coverage | Abstention rate |
| --- | ---: | ---: | ---: | --- | --- | --- |
| Baseline, all | 30 | 30 | 0 | 12/30 = 40% | 30/30 = 100% | 0/30 = 0% |
| ClaimTrace, all | 30 | 20 | 10 | 13/20 = 65% | 20/30 = 66.7% | 10/30 = 33.3% |
| ClaimTrace, case-derived | 15 | 14 | 1 | 7/14 = 50% | 14/15 = 93.3% | 1/15 = 6.7% |
| ClaimTrace, synthetic | 15 | 6 | 9 | 6/6 = 100% | 6/15 = 40% | 9/15 = 60% |

Source: [grouped summary](../results/test_summary.csv) and baseline predictions. Assessed-item agreement uses different denominators and is not a directly comparable overall accuracy. The synthetic 6/6 result excludes nine abstentions; case-derived examples do not establish generalisation to genuinely unseen cases.

Three-class Macro F1 averages the F1 scores of `high_risk`, `evidence_needed` and `low_risk` with equal weight, using all 30 examples. Abstentions count as misses for their true label. Undefined precision is set to zero. The [metric table](../results/test_metrics.csv) reports 40.5% for the baseline and 48.0% for ClaimTrace. ClaimTrace made 17 high-risk, three low-risk and zero evidence-needed predictions, plus ten abstentions. Evidence-needed reference support is 13, not zero; its model recall is zero.

## Chinese retrieval audit

The [ten-query audit](../evaluation/retrieval_audit_10.csv) uses selected case-derived development queries and saved [development retrieval output](../results/dev_retrieval.csv), not the locked test. Ten reviews are completed. Exact expected-case matches are 7/10; semantic relevance and support for a risk reminder are both 10/10 according to the human review fields. No new retrieval run was needed to build the audit. A different case ID can still be relevant; these selected examples do not estimate general retrieval accuracy or compare embedding models experimentally.

## Human review

The [review workbook](../evaluation/manual_review_20.xlsx) and [structured summary](../results/manual_review_summary.csv) record 20 completed reviews, split equally between the two source groups.

| Group | Reviewed | Supported / assessable present citations | Not applicable | Uncertain citation support |
| --- | ---: | --- | ---: | ---: |
| All | 20 | 10/11 = 90.9% | 9 | 0 |
| Case-derived | 10 | 8/9 = 88.9% | 1 | 0 |
| Synthetic | 10 | 2/2 = 100% | 8 | 0 |

The denominator includes only `citation_present=yes` and `citation_supported=yes` or `no`. It excludes `not_applicable` and `uncertain`, listed separately above. All 20 recommendation-actionability entries are `not_applicable` because historical outputs omit `next_action`; this is not evidence that recommendations were useful. Natural-language reviewer notes and final human labels are preserved. The earlier six-row `manual_review.csv` is not the completed review workbook.

## Costs and technical verification

[Request metadata](REQUEST_USAGE_EVIDENCE_EN.md) covers two later successful requests only: 1,869 tokens and service-reported US$0.00040545. Historical locked-test cost and end-to-end response time were not measured. See the [reproducibility record](REPRODUCTION_CHECK_EN.md) for offline software tests, which check implementation behaviour rather than model quality.
