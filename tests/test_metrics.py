"""Test metric definitions and locked-sample integrity without model calls."""

import pandas as pd
import pytest

import evaluation.metrics_test as metrics


def make_frames() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    claim_ids = [f"CLAIM-{index:03d}" for index in range(30)]
    labels = ["high_risk"] * 12 + ["evidence_needed"] * 13 + ["low_risk"] * 5
    locked = pd.DataFrame({"claim_id": claim_ids, "label": labels})
    baseline = pd.DataFrame(
        {
            "claim_id": claim_ids,
            "expected_label": labels,
            "predicted_label": labels,
        }
    )

    predictions = ["insufficient_evidence"] * 30
    predictions[0:10] = ["high_risk"] * 10
    predictions[12:19] = ["high_risk"] * 7
    predictions[19:25] = ["evidence_needed"] * 6
    predictions[25:30] = ["low_risk"] * 5
    claimtrace = pd.DataFrame(
        {
            "claim_id": claim_ids,
            "expected_label": labels,
            "predicted_label": predictions,
        }
    )
    return locked, baseline, claimtrace


def make_main_frames() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Use synthetic IDs to satisfy the CLI's saved-result consistency checks."""
    locked, baseline, claimtrace = make_frames()

    baseline_predictions = ["low_risk"] * 30
    baseline_predictions[0:3] = ["high_risk"] * 3
    baseline_predictions[3] = "evidence_needed"
    baseline_predictions[12:16] = ["evidence_needed"] * 4
    baseline["predicted_label"] = baseline_predictions

    claimtrace_predictions = ["insufficient_evidence"] * 30
    claimtrace_predictions[0:10] = ["high_risk"] * 10
    claimtrace_predictions[12:19] = ["high_risk"] * 7
    claimtrace_predictions[25:28] = ["low_risk"] * 3
    claimtrace["predicted_label"] = claimtrace_predictions
    return locked, baseline, claimtrace


def write_inputs(tmp_path, monkeypatch: pytest.MonkeyPatch, frames) -> None:
    locked, baseline, claimtrace = frames
    locked_path = tmp_path / "locked.csv"
    baseline_path = tmp_path / "baseline.csv"
    claimtrace_path = tmp_path / "claimtrace.csv"
    locked.to_csv(locked_path, index=False)
    baseline.to_csv(baseline_path, index=False)
    claimtrace.to_csv(claimtrace_path, index=False)
    monkeypatch.setattr(metrics, "LOCKED_TEST", locked_path)
    monkeypatch.setattr(metrics, "BASELINE_RESULTS", baseline_path)
    monkeypatch.setattr(metrics, "CLAIMTRACE_RESULTS", claimtrace_path)


def metric_value(rows: list[dict], metric_name: str, class_label: str = "") -> dict:
    selected = [
        row
        for row in rows
        if row["metric"] == metric_name and row["class_label"] == class_label
    ]
    assert len(selected) == 1
    return selected[0]


def test_load_and_validate_requires_same_30_unique_ids_and_locked_labels(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Requires both systems to match the same 30 unique locked IDs and labels."""
    frames = make_frames()
    write_inputs(tmp_path, monkeypatch, frames)

    locked, baseline, claimtrace = metrics.load_and_validate()

    assert len(locked) == len(baseline) == len(claimtrace) == 30
    assert locked["claim_id"].is_unique
    assert set(baseline["claim_id"]) == set(locked["claim_id"])
    assert set(claimtrace["claim_id"]) == set(locked["claim_id"])
    assert locked["label"].value_counts().to_dict() == {
        "high_risk": 12,
        "evidence_needed": 13,
        "low_risk": 5,
    }


@pytest.mark.parametrize(
    ("target", "mutation", "message"),
    [
        ("baseline", "duplicate", "duplicate claim_id"),
        ("claimtrace", "missing_extra", "claim_id set does not match"),
        ("baseline", "wrong_label", "expected labels do not match"),
        ("claimtrace", "short", "must contain 30 rows"),
    ],
)
def test_load_and_validate_rejects_wrong_sample_set_or_labels(
    target: str,
    mutation: str,
    message: str,
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rejects altered, incomplete, duplicate, or relabeled evaluation samples."""
    locked, baseline, claimtrace = make_frames()
    selected = baseline if target == "baseline" else claimtrace
    if mutation == "duplicate":
        selected.loc[1, "claim_id"] = selected.loc[0, "claim_id"]
    elif mutation == "missing_extra":
        selected.loc[0, "claim_id"] = "CLAIM-EXTRA"
    elif mutation == "wrong_label":
        selected.loc[0, "expected_label"] = "low_risk"
    else:
        selected.drop(index=selected.index[-1], inplace=True)
    frames = (locked, baseline, claimtrace)
    write_inputs(tmp_path, monkeypatch, frames)

    with pytest.raises(ValueError, match=message):
        metrics.load_and_validate()


def test_metric_denominators_and_abstentions_use_all_locked_rows() -> None:
    """Protects TP/FP/FN, three-class Macro F1, coverage, and abstention denominators."""
    locked, _, claimtrace = make_frames()

    rows = metrics.calculate_system_metrics("claimtrace", claimtrace, locked)
    precision = metric_value(rows, "precision", "high_risk")
    recall = metric_value(rows, "recall", "high_risk")
    f1 = metric_value(rows, "f1", "high_risk")
    macro_f1 = metric_value(rows, "macro_f1")
    coverage = metric_value(rows, "coverage_rate")
    abstention = metric_value(rows, "abstention_rate")

    assert (precision["numerator"], precision["denominator"]) == (10, 17)
    assert precision["value"] == pytest.approx(10 / 17)
    assert (recall["numerator"], recall["denominator"]) == (10, 12)
    assert recall["value"] == pytest.approx(10 / 12)
    assert f1["value"] == pytest.approx(2 * (10 / 17) * (10 / 12) / ((10 / 17) + (10 / 12)))
    assert (coverage["numerator"], coverage["denominator"]) == (28, 30)
    assert (abstention["numerator"], abstention["denominator"]) == (2, 30)
    assert macro_f1["scope"] == "three_reference_classes"
    assert macro_f1["value"] == pytest.approx(
        sum(
            metric_value(rows, "f1", label)["value"]
            for label in metrics.REFERENCE_LABELS
        )
        / 3
    )


def test_abstained_true_high_risk_rows_count_as_false_negatives() -> None:
    """Prevents abstentions on positive examples from inflating high-risk recall."""
    locked, _, claimtrace = make_frames()
    rows = metrics.calculate_system_metrics("claimtrace", claimtrace, locked)

    false_negatives = metric_value(rows, "fn", "high_risk")
    assert false_negatives["count"] == 2


def test_main_writes_generated_metrics_to_configured_temp_output(
    tmp_path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    """Checks CLI denominators and output without touching formal evaluation assets."""
    write_inputs(tmp_path, monkeypatch, make_main_frames())
    output_path = tmp_path / "generated_metrics.csv"
    monkeypatch.setattr(metrics, "OUTPUT", output_path)

    metrics.main()

    assert output_path.exists()
    generated = pd.read_csv(output_path)
    assert (
        generated["system"].eq("claimtrace")
        & generated["metric"].eq("coverage_rate")
    ).sum() == 1
    assert len(generated) == 59
    generated_rows = generated.fillna("").to_dict("records")
    for system, expected_precision, expected_recall in [
        ("rule_baseline", (3, 3), (3, 12)),
        ("claimtrace", (10, 17), (10, 12)),
    ]:
        system_rows = [row for row in generated_rows if row["system"] == system]
        precision = metric_value(system_rows, "precision", "high_risk")
        recall = metric_value(system_rows, "recall", "high_risk")
        assert (precision["numerator"], precision["denominator"]) == expected_precision
        assert (recall["numerator"], recall["denominator"]) == expected_recall
    claimtrace_rows = [row for row in generated_rows if row["system"] == "claimtrace"]
    abstention = metric_value(claimtrace_rows, "abstention_rate")
    assert (abstention["numerator"], abstention["denominator"]) == (10, 30)
    assert metric_value(claimtrace_rows, "coverage_rate")["value"] == pytest.approx(20 / 30)
    assert "high-risk precision=" in capsys.readouterr().out
