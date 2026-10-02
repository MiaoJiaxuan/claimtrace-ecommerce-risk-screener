# ClaimTrace Business and Technical Tradeoff Analysis

Miao Jiaxuan | PE6201

## Problem and intended users

ClaimTrace screens Chinese e-commerce advertising claims for small sellers. It combines a rule baseline, related enforcement cases and a model-generated risk card in one interface. The prototype improves access to contextual evidence, but its combined risk-detection recall of 68% falls short of the proposal's 80% target. This limits its usefulness as an automated screening system.

The problem comes from my previous product-copy editing work. I checked text against a company prohibited-words list, followed by a supervisor's review. I recall spending one to three minutes per item; this was not timed. Small sellers are the intended users, not an interviewed or validated customer segment. The proposed benefit is easier evidence assembly before human review, rather than proven time savings or replacement of that review.

Users enter one Chinese claim and receive a screening label, reasoning and retrieved evidence, or an insufficient-evidence response. The tool can identify dangerous medical-effect advertising in ordinary product copy, but offers no professional advice. Low risk is not legal approval, and publication requires human confirmation. A human-review prompt does not assign a reviewer or create a ticket.

## Build versus buy and technical choices

I built the Streamlit workflow, keyword rules, retrieval orchestration, response validation and evaluation. I reused Python libraries, multilingual embeddings and a hosted foundation model through OpenRouter. Buying model inference avoids training and hosting a language model, but introduces external-service dependence and requires scrutiny of generated reasoning.

The current retriever uses paraphrase-multilingual-MiniLM-L12-v2 and cosine similarity (src/retrieval.py). This addresses the teacher's concern about the proposal's English-trained MiniLM over Chinese text. The model card describes multilingual support, not performance on this project (Sentence Transformers, n.d.). With only 30 case records, direct cosine ranking is sufficient for this prototype; FAISS would add infrastructure without a demonstrated requirement. I did not train a classifier or implement an agent because the task follows a fixed retrieval-and-assessment sequence.

A selected audit reused saved retrieval results for ten Chinese development queries. Seven top-ranked case IDs matched the expected IDs; all ten were manually judged relevant and supportive of a risk reminder (evaluation/retrieval_audit_10.csv). A different ID is not necessarily irrelevant. However, this small, selected audit is neither a controlled embedding comparison nor a general retrieval-accuracy estimate.

The provisional threshold of 0.30 permits one model request at or above the score and abstains below it (src/risk_pipeline.py). It has not been calibrated. Pydantic checks response structure; current guards suppress non-verbatim highlighted text and citations whose title-and-URL pair is absent from retrieval. These checks reduce particular output errors, not unsupported reasoning. They were added after the saved evaluation and cannot be credited with improving its metrics. An independent LLM judge was not implemented; the recorded reviews are human assessments.

## Evaluation results and their implications

Both systems were evaluated on the same 30 locked items: 12 high_risk, 13 evidence_needed and five low_risk. Reference labels were frozen before testing and are project judgements, not regulator labels. The saved predictions and denominators are in evaluation/test_set_locked.csv, results/test_baseline.csv and results/test_full.csv.

| Positive class | System | Precision | Recall |
| --- | --- | ---: | ---: |
| High risk only | Rule baseline | 3/3 = 100% | 3/12 = 25% |
| High risk only | ClaimTrace | 10/17 = 58.8% | 10/12 = 83.3% |
| High risk plus evidence needed | Rule baseline | 8/8 = 100% | 8/25 = 32% |
| High risk plus evidence needed | ClaimTrace | 17/17 = 100% | 17/25 = 68% |

Precision is TP/(TP+FP), and recall is TP/(TP+FN). The proposal's 80% target concerns the combined class. The 83.3% high-risk recall cannot replace the unmet 68% combined result. Abstention is not automatic detection: a positive item returned as insufficient_evidence remains a false negative. ClaimTrace detects more high-risk items than the baseline, but its seven high-risk false positives would require reviewers to distinguish a warning from evidence of wrongdoing.

Three-class Macro F1 is 40.5% for the baseline and 48.0% for ClaimTrace, averaging F1 equally across the three reference labels and counting abstentions as misses for their true class (results/test_metrics.csv). ClaimTrace predicted no evidence_needed items despite 13 reference examples. The improvement therefore conceals a class-level failure. One additional miss changes high-risk recall by 8.3 percentage points, illustrating the estimate's sensitivity to this small sample.

Coverage is 20/30 (66.7%); abstention is 10/30 (33.3%). Label agreement among assessed items is 13/20 (65%), versus 12/30 (40%) for the baseline, so these percentages are not directly comparable. Case-derived items have 7/14 agreement and 14/15 coverage; synthetic items have 6/6 agreement but only 6/15 coverage. The nine synthetic abstentions prevent interpreting 6/6 as 100% accuracy on new claims (results/test_summary.csv). Case-derived success also does not establish generalisation to unseen cases.

Twenty human reviews cover ten items per source group. Citation support is 10/11 among present, assessable citations; nine records are not applicable. This is not overall citation accuracy. Recommendation actionability could not be assessed because historical outputs omit next_action (results/manual_review_summary.csv). Samples are partly synthetic, and no inter-rater reliability estimate is available. These weaknesses call for more independently labelled examples and a new holdout, not adjustments to the locked labels or test-set tuning.

## Cost privacy and next steps

Two subsequent successful requests used openai/gpt-4o-mini. Their non-content metadata are documented in docs/REQUEST_USAGE_EVIDENCE_EN.md; costs are service-returned usage.cost values, not price estimates (OpenRouter, n.d.).

| Date in 2026 | Input / output tokens | Cost in USD | Request time |
| --- | ---: | ---: | ---: |
| 30 September | 782 / 105 | 0.00018030 | 3.044005 s |
| 1 October | 809 / 173 | 0.00022515 | 3.827186 s |

Together, these calls used 1,869 tokens and cost US$0.00040545. Two observations cannot establish stable operating cost or the cost of the historical 30-item evaluation. Timings include HTTP handling and response validation, but exclude model loading, retrieval and page rendering. The logs contain no claim IDs, preventing independent mapping to particular development items.

Claims and retrieved case text leave the device for inference. Local logs omit that text and keys, but this does not remove the external disclosure. Users should exclude confidential content. Labour spent verifying warnings, service charges and maintenance would all enter an operating-cost model; without measured review time, traffic or wages, a return-on-investment calculation would be speculative.

The next evaluation should compare retrieval models and threshold settings on development data, freeze the selected version, then test a separately labelled holdout. In parallel, observed seller use should establish whether evidence assembly actually helps reviewers. For now, ClaimTrace demonstrates a functioning, testable review workflow, with insufficient evidence for autonomous compliance decisions or business savings.

## References

Sentence Transformers. (n.d.). *paraphrase-multilingual-MiniLM-L12-v2 model card*. Hugging Face. https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

OpenRouter. (n.d.). *API reference*. https://openrouter.ai/docs/api_reference/overview
