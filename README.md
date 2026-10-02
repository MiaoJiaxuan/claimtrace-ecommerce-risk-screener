# ClaimTrace

Evidence-based preliminary screening for Chinese e-commerce advertising claims.

ClaimTrace is a course prototype for small sellers preparing product-page copy. Enter a Chinese claim to inspect keyword-rule findings, related public enforcement cases and a structured screening result. The interface opens in English, with English explanations and case summaries. A Chinese interface is also available. Original claim spans and expandable source text preserve the Chinese evidence.

ClaimTrace supports preliminary review. A person must verify the claim and supporting records before publication. Case similarity measures textual relevance; the cited case provides context for that review.

## Start here

- **Problem statement:** [user need, workflow and evaluation objective](docs/PROBLEM_STATEMENT_EN.md).
- **Report:** [Business and technical tradeoff analysis (PDF)](docs/BUSINESS_TECHNICAL_TRADEOFF_EN.pdf).
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

Open `http://127.0.0.1:8501`. Leave the server terminal running; use another terminal for commands. Press Ctrl+C in the server terminal to stop it. Calling the environment's Python directly avoids PowerShell activation-policy issues.

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

Keep the real key in the local `.env` file, which Git ignores. Live screening sends the claim and retrieved case summaries to OpenRouter and incurs provider charges. Use non-confidential inputs.

Choose one of three examples or type a claim, then choose **Start risk review**. **Clear claim** resets the input and result. Language switching preserves input. An empty assessment displays a warning without loading the pipeline. Saved evaluation outputs can be inspected without configuring a key or running live screening.

## Offline automated tests

`pytest.ini` limits test discovery to `tests/`. The tests use mocked embeddings and model responses, so they run without API charges or model downloads.

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

The response schema contains risk level, highlighted claim, reason, citation title/URL, next action, confidence and abstention. Current guards suppress a highlighted span not copied from the input and a citation pair not found in retrieval. Reviewers check the factual support for the reasoning. The threshold remains provisional; confidence is the model's own score.

| Project reference label | Meaning within this prototype |
| --- | --- |
| `high_risk` | Expressions requiring priority scrutiny, such as strong cure guarantees or absolute claims. |
| `evidence_needed` | Claims about price, ranking, quantity or performance that require supporting records. |
| `low_risk` | No configured concern found within the prototype's limited scope; not approval. |

`insufficient_evidence` records abstention separately from the three project reference labels.

## Results on the locked 30-item set

Both systems use the same 30 IDs and frozen labels: **12 high risk, 13 evidence needed, 5 low risk**. The saved evaluation predates the later interface and response-validation changes.

| Positive class | Rule baseline Precision / Recall | ClaimTrace Precision / Recall |
| --- | --- | --- |
| High risk, 12 positives | 3/3 = 100% / 3/12 = 25% | 10/17 = 58.8% / 10/12 = 83.3% |
| High risk + evidence needed, 25 positives | 8/8 = 100% / 8/25 = 32% | 17/17 = 100% / 17/25 = 68% |

The original combined-class **80% recall target was not reached**. Abstentions on positive examples count as missed automatic detections. ClaimTrace predicted **no `evidence_needed` labels**.

| Measure | Rule baseline | ClaimTrace |
| --- | ---: | ---: |
| Three-reference-class Macro F1 | 40.5% | 48.0% |
| Coverage | 30/30 = 100% | 20/30 = 66.7% |
| Abstention / human-review prompt rate | 0/30 = 0% | 10/30 = 33.3% |
| Label agreement among assessed items | 12/30 = 40% | 13/20 = 65% |

Macro F1 averages the three reference-class F1 scores equally; abstentions count as misses for their true label, and undefined precision is set to zero. Assessed-item agreement uses different denominators across the two systems.

For case-derived items, agreement is 7/14 with coverage 14/15. For synthetic items, agreement is 6/6 with coverage 6/15 and nine abstentions. The [evidence guide](docs/EVALUATION_EVIDENCE_EN.md) provides source files, group denominators and audit results.

Ten selected Chinese development queries were manually checked: 7/10 exact case-ID matches and 10/10 judged relevant to a risk reminder. Twenty completed human reviews contain 11 assessable citations, of which 10 support the reminder; nine are not applicable. Recommendation actionability is unassessed because the historical outputs omit `next_action`. Both audits use small, selected samples.

## Code and evidence map

| Location | Responsibility |
| --- | --- |
| `app.py`, `src/ui_components.py`, `src/ui_text.py`, `tokens.css` | Bilingual Streamlit interface and presentation. |
| `src/case_display.py`, `assets/case-summaries-en.json` | English case display; original Chinese records remain the retrieval input. |
| `src/rules_baseline.py` | Independent keyword/pattern baseline. |
| `src/retrieval.py`, `src/risk_pipeline.py` | Case ranking and provisional abstention. |
| `src/schemas.py`, `src/llm_client.py` | Structured response validation and one-request model client. |
| `src/usage_logging.py` | Local metadata-only Token, cost and request-time logging. |
| `tests/` | Fixed-fixture, mocked offline unit tests. |
| `data/`, `evaluation/`, `results/` | Source summaries, reference labels, saved audits and historical predictions. |

The [evaluation guide](evaluation/README.md) lists each script's inputs and outputs. Use an isolated copy for experiments to preserve the saved evaluation.

## Provenance and operating limits

The author read the linked public case sources and wrote the case summaries. Source publisher, date, title and URL remain in `data/sources.csv`; original publishers retain rights in their material. Source reuse follows each publisher's terms. The [SVG illustration](assets/README.md) uses local vector shapes.

Two subsequent logged requests used 1,869 tokens with service-returned cost of **US$0.00040545**. Request times were 3.044005 and 3.827186 seconds, excluding retrieval and UI processing. These two observations are documented in the [request record](docs/REQUEST_USAGE_EVIDENCE_EN.md).

The report discusses the small, partly synthetic sample, threshold calibration and the need to measure seller review time in a future evaluation.
