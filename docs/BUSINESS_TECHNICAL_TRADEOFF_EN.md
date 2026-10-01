# ClaimTrace Business and Technical Trade-off Analysis

ClaimTrace is a working prototype for screening Chinese e-commerce product claims. Its current evidence does not meet the proposal's 80% recall target for high-risk and evidence-needed claims combined: observed recall is 68% on the locked 30-item set. The prototype can surface claims for review, but it cannot approve copy or replace a human decision.

## Problem and intended users

ClaimTrace is designed for small e-commerce sellers preparing Chinese product-page copy. The narrower assumption that some lack in-house compliance support has not been validated through seller interviews. In my previous copy-editing work, I checked claims against a company prohibited-words list before a supervisor reviewed them. I recall spending one to three minutes per item, but did not time it; this is personal context, not seller research or measured savings.

The prototype retrieves related public enforcement cases and returns a preliminary risk card. It can flag potentially risky claims, including cure or disease-prevention claims, but does not provide legal, medical, financial or other professional advice. `low_risk` is not legal approval; publication still requires human review. A review prompt does not create a ticket or assign a reviewer.

## Build versus buy and technical choices

I built the Streamlit workflow, rules, retrieval, threshold handling, response validation and evaluation, while reusing Python libraries, a multilingual embedder and a hosted model through OpenRouter. This avoids training and hosting a foundation model, but retains service, corpus and human-verification dependencies.

The retriever uses `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` with cosine similarity instead of the proposal's English-trained `all-MiniLM-L6-v2` and FAISS plan (`src/retrieval.py`; original problem statement). Its model card describes multilingual embeddings, not ClaimTrace quality (Sentence Transformers, n.d.). In a selected ten-query development audit, the top case ID matched the expected ID in 7/10 queries, while reviewers judged all ten relevant and supportive of a risk reminder; this is not a general accuracy estimate (`evaluation/retrieval_audit_10.csv`).

The uncalibrated 0.30 threshold abstains below the score and permits one model call at or above it; it is not an illegality probability (`src/risk_pipeline.py`). Schema validation checks structure, not factual truth. I did not implement FAISS, train a classifier or build an agent: the workflow is a fixed sequence, and an independent LLM judge remained an optional proposal. The twenty completed reviews were human reviews, not an LLM judge (`src/schemas.py`; `src/llm_client.py`; `evaluation/manual_review_20.xlsx`; `results/manual_review_summary.csv`).

## Evaluation results and trade-offs

The locked set contains 30 unique items: 12 `high_risk`, 13 `evidence_needed` and 5 `low_risk`. The rule baseline and ClaimTrace results use the same IDs and reference labels. These are project labels, not official regulator labels (`evaluation/test_set_locked.csv`; `results/test_baseline.csv`; `results/test_full.csv`; `results/test_metrics.csv`).

| Positive-class definition | System | Precision | Recall |
| --- | --- | ---: | ---: |
| `high_risk` only (12 positives) | Rule baseline | 3/3 = 100% | 3/12 = 25% |
| `high_risk` only (12 positives) | ClaimTrace | 10/17 = 58.8% | 10/12 = 83.3% |
| `high_risk` + `evidence_needed` (25 positives) | Rule baseline | 8/8 = 100% | 8/25 = 32% |
| `high_risk` + `evidence_needed` (25 positives) | ClaimTrace | 17/17 = 100% | 17/25 = 68% |

Precision is TP/(TP+FP); recall is TP/(TP+FN). The proposal set an 80% recall target for the combined risk/evidence-needed class. ClaimTrace's 68% does not meet it; the 83.3% high-risk-only result uses a different positive class and cannot substitute for the target. `insufficient_evidence` is an abstention, not an automatic detection, so a positive item referred for review counts as a missed detection in combined recall.

Three-class Macro F1, the unweighted mean across `high_risk`, `evidence_needed` and `low_risk`, was 40.5% for the baseline and 48.0% for ClaimTrace. ClaimTrace predicted no `evidence_needed` items. It covered 20/30 items (66.7%) and abstained on 10/30 (33.3%). Agreement with project labels among judged items was 13/20 (65.0%); the baseline agreed on 12/30 (40.0%). These different denominators make agreement rates non-comparable. ClaimTrace's higher recall came with lower coverage and more high-risk false positives (`results/test_metrics.csv`; `results/test_summary.csv`).

Human review covered 20 items (10 per source group). Ten of 11 applicable citations supported the reminder (90.9%); nine records had no applicable citation. This is not overall citation accuracy. Recommendation actionability remains unassessed because saved outputs lack `next_action`. The locked test shows judged agreement/coverage of 7/14 and 14/15 for case-derived items, and 6/6 with 6/15 for synthetic items (nine abstentions). Neither 6/6 nor these small audits establish generalisation (`results/manual_review_summary.csv`; `results/test_summary.csv`).

## Critical reflection and future direction

Before ClaimTrace, my own workflow checked product-page copy against a prohibited-words list and then sent it for supervisor review. The prototype puts rule matches, related public cases and a screening card in one view. This changes evidence assembly only: I have no seller interviews, deployment, timed comparison or adoption evidence, so cannot claim faster work or impact.

Thirty locked items cannot support broad claims: one miss changes high-risk recall by 8.3 percentage points and combined recall by 4 points. The same-set baseline is a reference, not evidence of marketplace performance. Macro F1 is modest at 48.0%, and the system's zero `evidence_needed` predictions reveal a class-level failure. Twenty human reviews and ten retrieval queries are small case audits; no inter-rater reliability statistic is available. Citation support of 10/11 applies only to applicable citations in the reviewed sample.

To address the English-model/Chinese-text mismatch raised in feedback, I replaced the proposal's English-trained MiniLM with a multilingual model and audited ten development queries; this was not a controlled model comparison. I did not tune the 0.30 threshold or use the locked set for tuning. New exact-span and source guards pass offline unit tests, but were not part of historical predictions and have no measured effect on reported metrics. Remaining issues include partly synthetic data, unverified source-reuse rights and link availability, and missing historical `next_action` fields.

The next step is to collect more independently labelled Chinese claims, compare retrieval and threshold settings on development data only, and evaluate a frozen version on a new holdout with documented human adjudication. Until then, these results support a prototype, not a production compliance claim; the original 80% combined-recall target remains unmet.

## Cost, privacy and conclusion

Two successful development-sample requests were logged for `openai/gpt-4o-mini`. The OpenRouter response usage fields include prompt, completion and total tokens and may include a cost value (OpenRouter, n.d.). The local log recorded:

| Request date | Input / output / total tokens | Provider-reported cost | Request-phase latency |
| --- | ---: | ---: | ---: |
| 30 Sep 2026 | 782 / 105 / 887 | US$0.0001803 | 3.044005 s |
| 1 Oct 2026 | 809 / 173 / 982 | US$0.00022515 | 3.827186 s |

Together, the two calls used 1,591 input and 278 output tokens and had a provider-reported cost of US$0.00040545. These observations do not represent the 30-item evaluation, a stable average or a forecast. The recorded latency covers the request phase, not retrieval, model loading or page rendering. The log stores neither claim text nor claim IDs, so it cannot independently identify which development items produced these calls (`logs/request_metrics.jsonl`; `src/usage_logging.py`).

The application sends the claim and retrieved case text to an external model service; omitting text from local logs does not keep request content on-device (`src/risk_pipeline.py`; `src/llm_client.py`). Users should not submit secrets or sensitive commercial information. Without measured seller traffic, wage data or timed review observations, I cannot calculate return on investment or claim a net time saving. The evidence supports a working prototype, not a production compliance service. Any model or threshold change should be tested on new, independently labelled claims; the locked set should remain untouched.

## References

Sentence Transformers. (n.d.). *paraphrase-multilingual-MiniLM-L12-v2 model card*. Hugging Face. https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

OpenRouter. (n.d.). *API reference*. https://openrouter.ai/docs/api_reference/overview
