# Installation and verification record

## Environment

Windows, Python 3.12.14. Dependencies were installed from `requirements.txt` in a fresh virtual environment on 1 October 2026. The final check on 2 October reported no broken requirements with `python -m pip check`.

## Offline tests

On 2 October 2026, the final source passed **43 tests, with no failures or skips, in 10.97 seconds**:

```powershell
python -B -m pytest -q -p no:cacheprovider --basetemp <new-writable-test-directory>
```

`pytest.ini` restricts discovery to `tests/`. Tests use mocked embeddings and model responses, with a network guard rejecting unmocked connections. Coverage includes schema validation, rule precedence, cosine ranking, the 0.2999/0.30 boundary, response grounding, usage logging and fixed-sample metric denominators.

## Interface and live screening

Streamlit was checked in a browser on 2 October. English is the default interface. English desktop and mobile layouts were inspected at 1440 and 375 pixels; neither had horizontal overflow. Example selection, clearing, language switching and empty-input handling were also checked during interface verification.

A live development example was submitted: `这套水乳可以彻底治愈皮肤红肿、瘙痒和痘痘。` The result was **high_risk**, with a top retrieval score of **0.3754**, an English explanation and recommended action, a verbatim highlighted claim, and a citation to **CASE002**. This is a functional smoke check, separate from the saved 30-item evaluation.

English display titles and summaries cover all 30 corpus records. Source cards retain the original Chinese text for inspection. Display translations do not alter retrieval inputs, model prompts, citation matching or saved predictions.

Screenshots: [English desktop](screenshots/home-en.jpg), [English mobile](screenshots/home-en-mobile.jpg), [live result](screenshots/review-en.jpg), [English case sources](screenshots/sources-en.jpg).

## Reproduction scope

The saved evaluation measures predictive quality; the checks above cover installation, code behaviour and live connectivity. Real screening requires embedding weights and an OpenRouter key. Dependencies are unpinned, so future installations may resolve differently.
