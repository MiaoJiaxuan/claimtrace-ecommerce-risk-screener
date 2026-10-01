# ClaimTrace demo script (English)

**Target recording length: 5–7 minutes.** The instructor accepts approximately 5 minutes ±3 minutes and reviews no more than the first 8 minutes. Keep the presenter's face and the relevant computer/mobile screen visible together during the explanation (for example, use a clear picture-in-picture camera overlay). Speak clearly and selectively; rehearse once with a timer.

The video has not yet been recorded. This script is a recording guide, not evidence that a video exists.

## Before recording

- Start the current app and the offline historical replay using the already prepared local verification setup. Do not submit a new live claim just to make a result appear.
- Keep a visible label on all saved-result replay: **“Historical result replay — no new model request.”** Distinguish it from the current UI and from a local loading/error mock.
- Frame the camera and screen so the presenter remains visible while the relevant interface is legible. Hide API settings, account details, personal paths, unrelated windows and any secret.
- Use the saved evidence table for metrics; do not display `.env`, raw logs containing machine paths, or any API credential.

## Suggested narration and timing

### 0:00–0:45 — Problem and boundary

**Show:** the current home page with its screening boundary notice.

**Say:**

> ClaimTrace is a prototype for a first-pass review of Chinese e-commerce product claims. I built it around a traceable path from the submitted wording to rules, similar public cases and a screening card. It does not decide legality or approve copy. Small sellers are the intended design persona, not a group I have validated through interviews.

### 0:45–1:35 — Current interface

**Show:** enter a sample through the example control, switch languages without losing the text, clear it, and demonstrate the empty-input response. Do not press the live assessment button with a non-empty claim during this segment.

**Say:**

> The screen keeps the input, three examples, clear action and primary assessment action visible. Language switching preserves the typed claim. This interaction walkthrough does not make a model request. The rule and evidence explanations are presented directly rather than hidden behind a series of menus.

### 1:35–2:45 — Historical result replay

**Show:** one matching saved example, one disagreement, and one abstention. Keep the historical-replay notice in frame.

**Say:**

> These are saved historical results, not new model outputs. The first example shows a risk reminder with a source. Similarity is a text score, not an illegality probability, and the case does not prove facts about this seller. The second example shows a disagreement between the project label and system label, so I am not selecting only a success. The third abstains because the top score is below the provisional 0.30 threshold; abstention does not mean safe.

> Current code suppresses a highlighted span unless it exactly appears in the input, and suppresses citations unless the title and URL match a retrieved record. Those guards have offline tests, but they have not been evaluated on a new locked set.

### 2:45–4:00 — Evaluation and critique

**Show:** the metric table in `docs/PRODUCT_DOCUMENTATION_EN.md` or the detailed evidence file.

**Say:**

> Both systems were compared on the same 30 locked items, including 12 high-risk positives. For the high-risk class, the rule baseline has 100% precision and 25% recall; ClaimTrace has 58.8% precision and 83.3% recall. The original combined target has 25 positives: ClaimTrace detects 17, so recall is 68%, not the 80% target. The high-risk-only recall cannot replace that target.

> Three-class Macro F1 is 48.0%, compared with 40.5% for the baseline. ClaimTrace did not predict `evidence_needed`; it covered 20 of 30 items and prompted human review for 10. These counts show a recall/coverage trade-off, not overall compliance performance. The 30 items are a small, partly synthetic project set, and the reviewed samples do not prove generalisation.

### 4:00–5:15 — Build versus buy, cost and limits

**Show:** the architecture diagram and the two-call cost table in the English report.

**Say:**

> I built the fixed workflow, rules, retrieval organisation and evaluation, while reusing a multilingual embedding model and a hosted model through OpenRouter. I did not train a new classifier or build an agent because the workflow is a fixed sequence. Two development calls have real service-reported usage and cost, but two observations are not a stable cost or latency estimate. We have no measured seller time savings or return on investment.

> The next step is a new independently labelled Chinese claim set, development-only threshold and model comparisons, and a frozen evaluation with documented human adjudication. I did not tune against the locked test set.

### 5:15–5:45 — Close

**Say:**

> ClaimTrace makes a potential review trail easier to inspect, but it does not replace a reviewer. Its combined recall target remains unmet, its threshold is provisional, and production use would require stronger data, permissions and independent validation. Thank you.

## Recording checklist

- Face and screen are visible together where the interface is being explained.
- Total duration is between 2 and 8 minutes; aim for 5–7 minutes.
- Replay/mock labels remain visible and are not described as live inference.
- Metrics use the reported denominators; the unmet 68% versus 80% target is explicit.
- No API key, private account data or unsupported legal, commercial or user claims appear.
- Video plays, voice is clear, and screen text can be read. The author must still record and submit the video.
