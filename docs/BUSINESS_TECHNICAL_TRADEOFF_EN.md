# ClaimTrace Business and Technical Tradeoff Analysis

Miao Jiaxuan | PE6201

## Problem and intended users

ClaimTrace helps small Chinese e-commerce sellers check advertising claims before publication. It combines keyword rules, public enforcement cases and a model-generated risk card. The system retrieved useful contextual evidence, but achieved 68% combined risk-detection recall against my 80% target. Its strongest current use is preparing evidence for a reviewer; reliable automatic screening needs further development.

The problem comes from my previous product-copy editing work. I checked text against a company prohibited-words list and then submitted it for supervisor review. I recall spending one to three minutes per item, although I did not time the process. I chose small sellers without dedicated compliance support as the design persona. Seller interviews and measured review times are still needed to test the proposed benefit.

A seller enters one Chinese claim and receives a risk label, highlighted wording, reasoning, a cited case and a suggested action. Weak retrieval produces an insufficient-evidence response. The seller remains responsible for arranging review before publication. The tool provides preliminary screening rather than legal approval.

## Build versus buy and technical choices

I built the rules, retrieval workflow, validation and evaluation, and used Streamlit for the interface. I reused multilingual embeddings and rented model inference through OpenRouter. This gives me control over the task-specific checks while avoiding the infrastructure needed to train and host a language model. The tradeoff is dependence on an external service for availability, data handling and generated reasoning.

The retriever uses paraphrase-multilingual-MiniLM-L12-v2 to embed Chinese claims and 30 case summaries. Cosine similarity ranks the top three cases. Multilingual support fits the input language better than the English-trained model in my original proposal (Sentence Transformers, n.d.). For this small corpus, direct ranking keeps indexing simple. I chose a fixed pipeline because each request follows the same sequence; autonomous planning would add complexity without a clear task benefit.

Ten selected Chinese development queries were reviewed against saved retrieval results. Seven top-ranked case IDs matched their expected IDs; all ten were judged relevant to a risk reminder. The three different IDs still concerned related issues. This is encouraging evidence for these queries, although the selected sample is small and does not compare alternative embedding models.

A provisional similarity threshold of 0.30 controls model access. Lower scores trigger abstention; scores at or above it permit one request. Pydantic validates the response structure. Additional guards require highlighted wording to appear in the input and citation pairs to appear in retrieval. Reviewers must still check whether the cited facts support the reasoning. These guards were added after the saved evaluation, so their effect on predictive quality remains unmeasured.

## Evaluation results and implications

I compared the rules and ClaimTrace on the same 30 locked items: 12 high_risk, 13 evidence_needed and five low_risk. Labels were frozen before testing. The reference set contains 15 case-derived and 15 synthetic claims. Row-level predictions are saved in results/test_baseline.csv and results/test_full.csv, with the fixed inputs in evaluation/test_set_locked.csv.

| Positive class | System | Precision | Recall |
| --- | --- | ---: | ---: |
| High risk only | Rule baseline | 3/3 = 100% | 3/12 = 25% |
| High risk only | ClaimTrace | 10/17 = 58.8% | 10/12 = 83.3% |
| High risk plus evidence needed | Rule baseline | 8/8 = 100% | 8/25 = 32% |
| High risk plus evidence needed | ClaimTrace | 17/17 = 100% | 17/25 = 68% |

Precision is TP/(TP+FP), and recall is TP/(TP+FN). My 80% target applies to the combined class. Positive items returned as insufficient_evidence count as missed automatic detections. ClaimTrace finds more risky claims than the rules, but its high-risk precision of 58.8% means seven warnings overstate the reference risk category. This creates additional work for reviewers. With only 12 high-risk positives, one missed item changes recall by 8.3 percentage points.

Three-class Macro F1 rises from 40.5% to 48.0%, averaging the three reference-class F1 scores equally and counting abstentions as misses. However, ClaimTrace produced zero evidence_needed predictions despite 13 reference examples. This class failure is the most important result: retrieval of a similar enforcement case can encourage a stronger judgement than the current claim supports. Price and performance claims need supporting records before they can be treated as false claims.

Coverage is 20/30 (66.7%), with ten abstentions. Among assessed items, label agreement is 13/20 (65%), compared with 12/30 (40%) for the rules. These denominators differ. The case-derived group achieves 7/14 agreement and 14/15 coverage. The synthetic group achieves 6/6 agreement with only 6/15 coverage. Its nine abstentions expose limited reach beyond familiar case wording. The case-derived examples also share source material with the corpus, which limits conclusions about unseen cases.

Twenty human reviews cover ten items from each source group. Ten of eleven assessable citations support the warning; nine records have no applicable citation. Historical outputs omit next_action, leaving recommendation actionability unassessed. The evaluation uses human review; an independent LLM judge was not implemented. The partly synthetic sample, incomplete generation records and absence of inter-rater checks constrain reproducibility and label reliability.

## Cost privacy and future work

Two later requests to openai/gpt-4o-mini produced the usage records below. Costs are the service-returned usage.cost values (OpenRouter, n.d.).

| Date in 2026 | Input / output tokens | Cost in USD | Request time |
| --- | ---: | ---: | ---: |
| 30 September | 782 / 105 | 0.00018030 | 3.044005 s |
| 1 October | 809 / 173 | 0.00022515 | 3.827186 s |

The two calls total 1,869 tokens and US$0.00040545, averaging about US$0.000203 per observed request. A forecast would multiply input and output token counts by their respective model rates, then add hosting, maintenance and reviewer time. Two observations give only an initial cost indication. Historical evaluation cost was not recorded, and request timing excludes embedding, retrieval and page rendering.

Claims and case summaries are sent to OpenRouter for inference. The application asks users to exclude confidential content and stores only request metadata locally. External disclosure remains a deployment consideration. Labour could dominate the small inference charge because every publication decision still needs human confirmation; measured review times are therefore necessary for a business case.

My next step is to compare retrieval models and thresholds on development data, freeze a version and evaluate a separately labelled holdout. I would prioritise evidence_needed errors and the usefulness of next-action recommendations. Observed seller use should then establish whether the evidence trail reduces review effort enough to justify operating and maintenance costs.

## References

Sentence Transformers. (n.d.). *paraphrase-multilingual-MiniLM-L12-v2 model card*. Hugging Face. https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

OpenRouter. (n.d.). *API reference*. https://openrouter.ai/docs/api_reference/overview
