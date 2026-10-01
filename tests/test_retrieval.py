"""Test retrieval ranking with deterministic local fake embeddings."""

import numpy as np
import pandas as pd
import pytest

import src.retrieval as retrieval


class FakeEncoder:
    def __init__(self) -> None:
        self.calls: list[tuple[list[str], bool]] = []
        self.vectors = {
            "Alpha Case Summary A": [1.0, 0.0],
            "Beta Case Summary B": [0.0, 1.0],
            "Gamma Case Summary C": [0.6, 0.8],
            "claim": [1.0, 0.0],
        }

    def encode(self, texts: list[str], normalize_embeddings: bool) -> np.ndarray:
        self.calls.append((texts, normalize_embeddings))
        return np.asarray([self.vectors[text] for text in texts], dtype=float)


def case_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "case_id": "CASE-A",
                "publisher": "Agency",
                "publish_date": "2025-01-01",
                "title": "Alpha Case",
                "case_text": "Summary A",
                "risk_type": "price",
                "source_url": "https://example.invalid/a",
            },
            {
                "case_id": "CASE-B",
                "publisher": "Agency",
                "publish_date": "2025-01-02",
                "title": "Beta Case",
                "case_text": "Summary B",
                "risk_type": "health",
                "source_url": "https://example.invalid/b",
            },
            {
                "case_id": "CASE-C",
                "publisher": "Agency",
                "publish_date": "2025-01-03",
                "title": "Gamma Case",
                "case_text": "Summary C",
                "risk_type": "sales",
                "source_url": "https://example.invalid/c",
            },
        ]
    )


def test_retrieve_uses_fake_embeddings_for_local_cosine_ranking(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Protects deterministic cosine ranking, result shape, and top-k behavior offline."""
    source_path = tmp_path / "sources.csv"
    case_frame().to_csv(source_path, index=False)
    encoder = FakeEncoder()
    monkeypatch.setattr(retrieval, "SentenceTransformer", lambda _name: encoder)

    retriever = retrieval.CaseRetriever(str(source_path), model_name="offline-fake")
    results = retriever.retrieve("claim", top_k=2)

    assert [row["case_id"] for row in results] == ["CASE-A", "CASE-C"]
    assert [row["similarity_score"] for row in results] == [1.0, 0.6]
    assert set(results[0]) == {
        "case_id",
        "title",
        "case_text",
        "risk_type",
        "source_url",
        "similarity_score",
    }
    assert all(normalized for _, normalized in encoder.calls)


def test_empty_query_returns_empty_without_encoding_query(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Ensures blank claims do not trigger query encoding or fabricated evidence."""
    source_path = tmp_path / "sources.csv"
    case_frame().to_csv(source_path, index=False)
    encoder = FakeEncoder()
    monkeypatch.setattr(retrieval, "SentenceTransformer", lambda _name: encoder)
    retriever = retrieval.CaseRetriever(str(source_path), model_name="offline-fake")
    calls_after_initialization = len(encoder.calls)

    assert retriever.retrieve("  ") == []
    assert len(encoder.calls) == calls_after_initialization


def test_empty_case_file_is_rejected_before_model_construction(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Rejects an empty evidence corpus before constructing any embedding model."""
    source_path = tmp_path / "empty.csv"
    case_frame().iloc[0:0].to_csv(source_path, index=False)
    monkeypatch.setattr(
        retrieval,
        "SentenceTransformer",
        lambda _name: pytest.fail("model must not be constructed for empty data"),
    )

    with pytest.raises(ValueError, match="does not contain any cases"):
        retrieval.CaseRetriever(str(source_path))


def test_missing_required_column_is_rejected(tmp_path) -> None:
    """Prevents malformed case data from silently weakening retrieval evidence."""
    source_path = tmp_path / "missing.csv"
    case_frame().drop(columns=["source_url"]).to_csv(source_path, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        retrieval.CaseRetriever(str(source_path))
