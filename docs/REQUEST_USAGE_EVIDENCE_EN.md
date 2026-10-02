# Small-sample OpenRouter request metadata

This table transcribes only non-content fields from two successful records in the local, Git-ignored `logs/request_metrics.jsonl`, checked on 1 October 2026. The raw log, submitted claims, retrieved case text and API key are not included. The log does not record `claim_id`, so these requests cannot be independently mapped to a specific development claim from this table. No model request was made to prepare this document.

| UTC timestamp | Requested / returned model | Input tokens | Output tokens | Total tokens | Provider-reported cost (USD) | Request-stage time (s) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 2026-09-30 11:08:18.620 | `openai/gpt-4o-mini` / same | 782 | 105 | 887 | 0.00018030 | 3.044005 |
| 2026-10-01 04:16:13.642 | `openai/gpt-4o-mini` / same | 809 | 173 | 982 | 0.00022515 | 3.827186 |
| **Two-request total** | — | **1,591** | **278** | **1,869** | **0.00040545** | — |

`src/llm_client.py` starts its timer immediately before the HTTP request and stops after response parsing, citation/span guards and Pydantic validation. It excludes embedding-model load, retrieval, rule checks, Streamlit processing and rendering. The cost is the service response's `usage.cost` value, **not** a price-list estimate; `estimated_cost_usd`, `pricing_source` and `pricing_date` were absent. The two observations do not establish the cost of the historical 30-item locked evaluation, a stable per-request average, or end-to-end page latency. The raw local log would be needed to independently audit the transcription; it remains excluded from Git for privacy.
