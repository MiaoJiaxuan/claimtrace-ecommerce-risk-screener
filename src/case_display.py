"""English display summaries keyed to the unchanged Chinese retrieval corpus."""

import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def _translations() -> dict:
    path = Path(__file__).resolve().parents[1] / "assets" / "case-summaries-en.json"
    return json.loads(path.read_text(encoding="utf-8"))


def display_case(case: dict, lang: str) -> dict:
    """Return a presentation copy; retrieval and citation validation use originals."""
    translated = _translations().get(case.get("case_id"), {}) if lang == "en" else {}
    return {**case, **translated}
