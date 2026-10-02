# OpenRouter request usage

Two successful requests recorded on 30 September and 1 October 2026 provide the token, cost and request-time observations below. Values come from the local request log; claims and API keys are excluded.

| UTC timestamp | Requested / returned model | Input tokens | Output tokens | Total tokens | Provider-reported cost (USD) | Request-stage time (s) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 2026-09-30 11:08:18.620 | `openai/gpt-4o-mini` / same | 782 | 105 | 887 | 0.00018030 | 3.044005 |
| 2026-10-01 04:16:13.642 | `openai/gpt-4o-mini` / same | 809 | 173 | 982 | 0.00022515 | 3.827186 |
| **Two-request total** | — | **1,591** | **278** | **1,869** | **0.00040545** | — |

The timer in `src/llm_client.py` covers the HTTP request, response parsing and validation. Embedding, retrieval and page rendering are outside this interval. Cost is the service-returned `usage.cost` value.

These two observations total US$0.00040545, averaging US$0.000202725 per request. A forecast requires representative traffic and current input/output token prices, plus hosting and reviewer time. The historical 30-item evaluation has no recorded cost. Claim IDs were not logged for these two requests, so their association with development examples is unavailable.
