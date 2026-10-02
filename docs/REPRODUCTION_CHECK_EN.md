# Installation and verification record

Verified on 1 October 2026 on Windows with Python 3.12.14. A fresh virtual environment was created for a local Git clone, and dependencies were installed from `requirements.txt`. Installation and `pip check` succeeded. The same isolated environment was used to verify the final working files after the documentation and illustration cleanup.

## Offline tests

The final-file run completed with **43 passed, 0 failed and 0 skipped** in 41.19 seconds. The command was:

```powershell
$env:HF_HUB_OFFLINE = '1'
$env:TRANSFORMERS_OFFLINE = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHON_DOTENV_DISABLED = '1'
python -B -m pytest -q -p no:cacheprovider --basetemp <new-writable-test-directory> tests
```

Use the isolated environment's Python and a new dedicated temporary directory. Tests mock embedding and model responses; a network guard rejects unmocked connections. No `.env` was copied into the isolated environment, no model was downloaded, and no OpenRouter request or formal evaluation was run.

On 2 October 2026, the submission ZIP was extracted into a new directory and its code was tested with the same isolated environment: **43 passed, 0 failed and 0 skipped** in 10.90 seconds. This additionally checks that the packaged source includes the files needed by the offline tests.

Tests cover schema validation, rule precedence, cosine ranking, the 0.2999/0.30 boundary, model response and citation handling, usage logging, and fixed-sample metric denominators. Passing unit tests does not establish predictive quality; the [saved evaluation evidence](EVALUATION_EVIDENCE_EN.md) addresses that separately.

## Current interface

Streamlit started on loopback using the final working files. A real-browser smoke check confirmed:

- Chinese and English home pages and the original local SVG render.
- Language switching preserves entered text.
- An example fills the input; Clear claim removes it.
- An empty request displays a warning without running the pipeline.
- At 320, 375, 768 and 1440px widths, the document has no horizontal overflow in either language.
- No browser-console errors were captured during these checks.

Current screenshots: [English desktop](screenshots/home-en.jpg), [Chinese desktop](screenshots/home-zh.jpg), [English mobile](screenshots/home-en-mobile.jpg).

No non-empty request was submitted in this check. This is a focused interface smoke test, not a full accessibility audit or a new live-output evaluation.

## Reproduction scope

This record verifies a clean local-clone installation and subsequent checks of the final working files, not an independent installation on the assessor's computer. Dependencies are unpinned, so future resolution may differ. Real screening additionally requires embedding weights and a configured OpenRouter key. The README separates these optional paid operations from the safe startup and offline-test commands.
