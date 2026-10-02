# ClaimTrace

Evidence-based preliminary screening for Chinese e-commerce advertising claims.

ClaimTrace is a course prototype for small sellers preparing product-page copy. Enter a Chinese claim to inspect keyword-rule findings, related public enforcement cases and a structured screening result. The interface supports Chinese and English; model explanations are requested in English and external case text is not automatically translated.

This tool does not provide legal advice or approve copy. Low risk is not legal approval; publication still requires human confirmation. Similarity is not an illegality probability, and a similar case does not prove wrongdoing by the current seller. A human-review prompt is not an assigned task or ticket.

## Start here

- **Report:** [PDF](docs/BUSINESS_TECHNICAL_TRADEOFF_EN.pdf), [Word](docs/BUSINESS_TECHNICAL_TRADEOFF_EN.docx), [Markdown](docs/BUSINESS_TECHNICAL_TRADEOFF_EN.md).
- **Product:** [persona, inputs, outputs and architecture](docs/PRODUCT_DOCUMENTATION_EN.md).
- **Evidence:** [data guide](data/README.md), [evaluation guide](evaluation/README.md), [saved results](results/README.md), [metrics and denominators](docs/EVALUATION_EVIDENCE_EN.md).
- **Verification:** [installation and offline checks](docs/REPRODUCTION_CHECK_EN.md), [two-request usage record](docs/REQUEST_USAGE_EVIDENCE_EN.md).

## Install and open the application

Python 3.12 is the verified environment. Install dependencies with internet access. Run all commands from the repository root. The initial page and offline tests need no API key or embedding-model download. Assessing non-empty text loads the multilingual embedding model, downloads its weights if not cached, and can make a paid OpenRouter request.

### Windows PowerShell

```powershell
git clone https://github.com/MiaoJiaxuan/claimtrace-ecommerce-risk-screener.git
cd claimtrace-ecommerce-risk-screener
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Open `http://127.0.0.1:8501`. Leave the server terminal running; use another terminal for commands. Press Ctrl+C in the server terminal to stop it. Calling the environment's Python directly avoids PowerShell activation-policy issues. If an old environment points to a removed interpreter, create a new environment with an installed Python rather than editing its launcher.

### macOS or Linux

```bash
git clone https://github.com/MiaoJiaxuan/claimtrace-ecommerce-risk-screener.git
cd claimtrace-ecommerce-risk-screener
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1
```

The macOS/Linux commands are the platform equivalents; the recorded installation check used Windows. Dependencies are not version-pinned, so future installations can resolve differently.

### Optional live screening

Only configure a key if you intend to make requests. Copy `.env.example` to `.env` if `.env` does not already exist, then edit the local file:

```dotenv
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Do not put a real key in `.env.example`, screenshots, Git or a submitted archive. A live request sends the claim and retrieved case summaries to OpenRouter. Do not submit personal data, secrets or confidential commercial copy. Provider billing applies; the app is not a hard spending-limit mechanism.

Choose one of three examples or type a claim, then choose **Start risk review / 开始风险审查**. **Clear claim / 清空文案** resets the input and result. Language switching preserves input. An empty assessment displays a warning without loading the pipeline. Saved evaluation outputs can be inspected without configuring a key or running live screening.

## Offline automated tests

Run only `tests/`. Bare `pytest` at the repository root can collect evaluation scripts with file-writing or model-calling side effects.

```powershell
$env:HF_HUB_OFFLINE = '1'
$env:TRANSFORMERS_OFFLINE = '1'
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider tests
```

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 .venv/bin/python -B -m pytest -q -p no:cacheprovider tests
```

Fixtures replace model responses and embedding vectors. The test network guard rejects unmocked socket/HTTP connections. Coverage includes schema validation, rule precedence, retrieval ranking, the 0.2999/0.30 threshold boundary, response grounding, usage logging and fixed-sample metric denominators. See the [verification record](docs/REPRODUCTION_CHECK_EN.md) for the executed result and environment. If pytest cannot access its system temporary directory, add `--basetemp <a-new-writable-temporary-directory>`; use a dedicated new directory because pytest owns its contents.

## How screening works

1. Keyword rules independently identify configured expressions.
2. `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` embeds the claim and the 30-case corpus; cosine ranking returns up to three cases.
3. Below the provisional **0.30** top score, the pipeline returns `insufficient_evidence` without calling the language model. At or above it, the pipeline allows one model request. The model can also abstain.

The response schema contains risk level, highlighted claim, reason, citation title/URL, next action, confidence and abstention. Current guards suppress a highlighted span not copied from the input and a citation pair not found in retrieval. They do not establish factual support for the reasoning. The threshold is not calibrated, and model self-reported confidence is not a probability of illegality.

| Project reference label | Meaning within this prototype |
| --- | --- |
| `high_risk` | Expressions requiring priority scrutiny, such as strong cure guarantees or absolute claims. |
| `evidence_needed` | Claims about price, ranking, quantity or performance that require supporting records. |
| `low_risk` | No configured concern found within the prototype's limited scope; not approval. |

`insufficient_evidence` is a system abstention output, not a fourth project reference label. These are project labels, not official regulatory decisions.

## Results on the locked 30-item set

Both systems use the same 30 IDs and frozen labels: **12 high risk, 13 evidence needed, 5 low risk**. These are saved historical predictions, not a new evaluation of subsequent interface or response-guard changes.

| Positive class | Rule baseline Precision / Recall | ClaimTrace Precision / Recall |
| --- | --- | --- |
| High risk, 12 positives | 3/3 = 100% / 3/12 = 25% | 10/17 = 58.8% / 10/12 = 83.3% |
| High risk + evidence needed, 25 positives | 8/8 = 100% / 8/25 = 32% | 17/17 = 100% / 17/25 = 68% |

The original combined-class **80% recall target was not reached**. The high-risk-only 83.3% result cannot substitute for it. Abstentions on positive examples count as missed automatic detections. ClaimTrace predicted **no `evidence_needed` labels**.

| Measure | Rule baseline | ClaimTrace |
| --- | ---: | ---: |
| Three-reference-class Macro F1 | 40.5% | 48.0% |
| Coverage | 30/30 = 100% | 20/30 = 66.7% |
| Abstention / human-review prompt rate | 0/30 = 0% | 10/30 = 33.3% |
| Label agreement among assessed items | 12/30 = 40% | 13/20 = 65% |

Macro F1 averages the three reference-class F1 scores equally; abstentions count as misses for their true label, and undefined precision is set to zero. Agreement among assessed items has different denominators across systems and is not a like-for-like overall accuracy comparison.

For case-derived items, agreement is 7/14 with coverage 14/15. For synthetic items, agreement is 6/6 with coverage 6/15 and nine abstentions; this is not 100% accuracy on new claims. The [evidence guide](docs/EVALUATION_EVIDENCE_EN.md) provides source files, group denominators and audit results.

Ten selected Chinese development queries were manually checked: 7/10 exact case-ID matches and 10/10 judged relevant to a risk reminder. Twenty completed human reviews contain 11 assessable citations, of which 10 support the reminder; nine are not applicable. Recommendation actionability is unassessed because the historical outputs omit `next_action`. These small audits are not population-wide estimates.

## Code and evidence map

| Location | Responsibility |
| --- | --- |
| `app.py`, `src/ui_components.py`, `src/ui_text.py`, `tokens.css` | Bilingual Streamlit interface and presentation. |
| `src/rules_baseline.py` | Independent keyword/pattern baseline. |
| `src/retrieval.py`, `src/risk_pipeline.py` | Case ranking and provisional abstention. |
| `src/schemas.py`, `src/llm_client.py` | Structured response validation and one-request model client. |
| `src/usage_logging.py` | Local metadata-only Token, cost and request-time logging. |
| `tests/` | Fixed-fixture, mocked offline unit tests. |
| `data/`, `evaluation/`, `results/` | Source summaries, reference labels, saved audits and historical predictions. |

Several evaluation scripts write results or make model calls. Read [their side-effect inventory](evaluation/README.md) before running them. Do not rerun the locked test or overwrite saved outputs as an installation check.

## Provenance and operating limits

The author read the linked public case sources and wrote the case summaries. Source publisher, date, title and URL remain in `data/sources.csv`; original publishers retain rights in their material. No blanket redistribution licence for third-party content is asserted. The [local SVG illustration](assets/README.md) contains no third-party image assets.

Two subsequent logged requests used 1,869 tokens with service-returned cost of **US$0.00040545**. Request times were 3.044005 and 3.827186 seconds, excluding retrieval and UI processing. This is neither the historical evaluation cost nor a stable operating-cost estimate; see [request metadata](docs/REQUEST_USAGE_EVIDENCE_EN.md).

The sample is partly synthetic, the case corpus is small and the threshold remains provisional. There is no measured seller time saving, ROI or broad generalisation result. The report explains these limitations and the next evaluation design.
