"""Privacy-minimised local metrics logging for future model requests."""

import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


DEFAULT_METRICS_LOG = (
    Path(__file__).resolve().parents[1] / "logs" / "request_metrics.jsonl"
)


def _number_or_none(value: object) -> int | float | None:
    """Return a finite JSON number without inventing missing usage values."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if not math.isfinite(value):
        return None
    return value


def make_request_metrics(
    *,
    model_requested: str,
    model_returned: object,
    usage: object,
    latency_seconds: float,
    request_status: str,
    error_type: str | None,
) -> dict:
    """Build one safe metrics event from response metadata only.

    Provider-reported ``usage.cost`` is stored separately from estimates.
    No estimate is calculated until a dated, documented price source exists.
    """
    usage_data = usage if isinstance(usage, dict) else {}
    returned_model = (
        model_returned if isinstance(model_returned, str) else None
    )

    return {
        "schema_version": 1,
        "request_id": str(uuid4()),
        "timestamp_utc": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
        "model_requested": model_requested,
        "model_returned": returned_model,
        "prompt_tokens": _number_or_none(usage_data.get("prompt_tokens")),
        "completion_tokens": _number_or_none(
            usage_data.get("completion_tokens")
        ),
        "total_tokens": _number_or_none(usage_data.get("total_tokens")),
        "provider_cost_usd": _number_or_none(usage_data.get("cost")),
        "estimated_cost_usd": None,
        "pricing_source": None,
        "pricing_date": None,
        "latency_seconds": round(max(latency_seconds, 0.0), 6),
        "request_status": request_status,
        "error_type": error_type,
    }


def append_request_metrics(event: dict) -> None:
    """Append one event to a local JSONL file.

    The caller is responsible for ensuring that the event contains metadata
    only. The log path may be overridden for local tests and deployments.
    """
    log_path = Path(
        os.getenv("CLAIMTRACE_METRICS_LOG_PATH", str(DEFAULT_METRICS_LOG))
    )
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", newline="\n") as log_file:
        log_file.write(
            json.dumps(event, ensure_ascii=False, separators=(",", ":"))
            + "\n"
        )
