"""Compute locked-test metrics from saved results without calling any model."""

from pathlib import Path

import pandas as pd


LOCKED_TEST = Path("evaluation/test_set_locked.csv")
BASELINE_RESULTS = Path("results/test_baseline.csv")
CLAIMTRACE_RESULTS = Path("results/test_full.csv")
OUTPUT = Path("results/test_metrics.csv")

REFERENCE_LABELS = ["high_risk", "evidence_needed", "low_risk"]
ABSTENTION_LABEL = "insufficient_evidence"


def load_and_validate() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the three saved inputs and verify their sample sets."""
    locked = pd.read_csv(LOCKED_TEST)
    baseline = pd.read_csv(BASELINE_RESULTS)
    claimtrace = pd.read_csv(CLAIMTRACE_RESULTS)

    for name, frame in {
        "locked_test": locked,
        "rule_baseline": baseline,
        "claimtrace": claimtrace,
    }.items():
        if len(frame) != 30:
            raise ValueError(f"{name} must contain 30 rows, found {len(frame)}")
        if frame["claim_id"].duplicated().any():
            raise ValueError(f"{name} contains duplicate claim_id values")

    expected_ids = set(locked["claim_id"])
    for name, frame in {
        "rule_baseline": baseline,
        "claimtrace": claimtrace,
    }.items():
        if set(frame["claim_id"]) != expected_ids:
            raise ValueError(f"{name} claim_id set does not match the locked test")

    locked_labels = locked.set_index("claim_id")["label"].sort_index()
    for name, frame in {
        "rule_baseline": baseline,
        "claimtrace": claimtrace,
    }.items():
        saved_labels = frame.set_index("claim_id")["expected_label"].sort_index()
        if not saved_labels.equals(locked_labels):
            raise ValueError(f"{name} expected labels do not match the locked test")

    label_counts = locked["label"].value_counts().to_dict()
    expected_counts = {"high_risk": 12, "evidence_needed": 13, "low_risk": 5}
    if label_counts != expected_counts:
        raise ValueError(
            f"Locked-test label counts differ from the checked values: {label_counts}"
        )

    return locked, baseline, claimtrace


def safe_rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def metric_row(
    system: str,
    scope: str,
    metric: str,
    *,
    class_label: str = "",
    count: int | None = None,
    numerator: int | None = None,
    denominator: int | None = None,
    value: float | None = None,
    definition: str = "",
) -> dict:
    return {
        "system": system,
        "scope": scope,
        "metric": metric,
        "class_label": class_label,
        "count": count,
        "numerator": numerator,
        "denominator": denominator,
        "value": value,
        "definition": definition,
    }


def calculate_system_metrics(
    system: str,
    frame: pd.DataFrame,
    locked: pd.DataFrame,
) -> list[dict]:
    """Calculate fixed-class metrics on all 30 locked-test records."""
    merged = locked[["claim_id", "label"]].merge(
        frame[["claim_id", "predicted_label"]],
        on="claim_id",
        how="inner",
        validate="one_to_one",
    )
    rows: list[dict] = []

    for label in REFERENCE_LABELS:
        actual_positive = merged["label"].eq(label)
        predicted_positive = merged["predicted_label"].eq(label)
        tp = int((actual_positive & predicted_positive).sum())
        fp = int((~actual_positive & predicted_positive).sum())
        fn = int((actual_positive & ~predicted_positive).sum())
        tn = int((~actual_positive & ~predicted_positive).sum())
        precision = safe_rate(tp, tp + fp)
        recall = safe_rate(tp, tp + fn)
        f1 = safe_rate(2 * precision * recall, precision + recall)

        for metric, count in {"tp": tp, "fp": fp, "tn": tn, "fn": fn}.items():
            rows.append(
                metric_row(system, "one_vs_rest", metric, class_label=label, count=count)
            )
        rows.extend(
            [
                metric_row(
                    system,
                    "one_vs_rest",
                    "precision",
                    class_label=label,
                    numerator=tp,
                    denominator=tp + fp,
                    value=precision,
                    definition="TP / (TP + FP)",
                ),
                metric_row(
                    system,
                    "one_vs_rest",
                    "recall",
                    class_label=label,
                    numerator=tp,
                    denominator=tp + fn,
                    value=recall,
                    definition="TP / (TP + FN)",
                ),
                metric_row(
                    system,
                    "one_vs_rest",
                    "f1",
                    class_label=label,
                    value=f1,
                    definition="Harmonic mean of precision and recall",
                ),
            ]
        )

    class_f1 = [
        row["value"]
        for row in rows
        if row["metric"] == "f1" and row["class_label"] in REFERENCE_LABELS
    ]
    rows.append(
        metric_row(
            system,
            "three_reference_classes",
            "macro_f1",
            value=sum(class_f1) / len(REFERENCE_LABELS),
            definition=(
                "Unweighted mean of F1 for high_risk, evidence_needed and "
                "low_risk; insufficient_evidence counts as a miss for its true class"
            ),
        )
    )

    predicted_counts = merged["predicted_label"].value_counts().to_dict()
    for label in [*REFERENCE_LABELS, ABSTENTION_LABEL]:
        rows.append(
            metric_row(
                system,
                "prediction_distribution",
                "predicted_count",
                class_label=label,
                count=int(predicted_counts.get(label, 0)),
            )
        )

    abstentions = int(merged["predicted_label"].eq(ABSTENTION_LABEL).sum())
    covered = len(merged) - abstentions
    rows.extend(
        [
            metric_row(
                system,
                "all_locked_test",
                "coverage_rate",
                numerator=covered,
                denominator=len(merged),
                value=safe_rate(covered, len(merged)),
                definition="Non-abstained predictions / all locked-test records",
            ),
            metric_row(
                system,
                "all_locked_test",
                "abstention_rate",
                numerator=abstentions,
                denominator=len(merged),
                value=safe_rate(abstentions, len(merged)),
                definition="insufficient_evidence predictions / all locked-test records",
            ),
        ]
    )
    return rows


def main() -> None:
    locked, baseline, claimtrace = load_and_validate()
    rows: list[dict] = []

    for label in REFERENCE_LABELS:
        rows.append(
            metric_row(
                "reference",
                "locked_test_distribution",
                "actual_count",
                class_label=label,
                count=int(locked["label"].eq(label).sum()),
            )
        )

    rows.extend(calculate_system_metrics("rule_baseline", baseline, locked))
    rows.extend(calculate_system_metrics("claimtrace", claimtrace, locked))
    output = pd.DataFrame(rows)

    def checked_value(system: str, metric: str, class_label: str = "") -> float:
        selected = output[
            output["system"].eq(system)
            & output["metric"].eq(metric)
            & output["class_label"].eq(class_label)
        ]
        if len(selected) != 1:
            raise ValueError(f"Expected one row for {system}/{metric}/{class_label}")
        return float(selected.iloc[0]["value"])

    expected_checks = {
        ("rule_baseline", "precision", "high_risk"): 1.0,
        ("rule_baseline", "recall", "high_risk"): 0.25,
        ("claimtrace", "precision", "high_risk"): 10 / 17,
        ("claimtrace", "recall", "high_risk"): 10 / 12,
        ("claimtrace", "abstention_rate", ""): 10 / 30,
    }
    for key, expected in expected_checks.items():
        actual = checked_value(*key)
        if abs(actual - expected) > 1e-12:
            raise ValueError(f"Checked value differs for {key}: {actual} != {expected}")

    OUTPUT.parent.mkdir(exist_ok=True)
    output.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

    print("Locked test: 30 unique records")
    print("Reference labels: high_risk=12, evidence_needed=13, low_risk=5")
    for system in ["rule_baseline", "claimtrace"]:
        precision = checked_value(system, "precision", "high_risk")
        recall = checked_value(system, "recall", "high_risk")
        f1 = checked_value(system, "f1", "high_risk")
        macro = checked_value(system, "macro_f1")
        abstention = checked_value(system, "abstention_rate")
        print(
            f"{system}: high-risk precision={precision:.1%}, "
            f"recall={recall:.1%}, F1={f1:.1%}, "
            f"macro F1={macro:.1%}, abstention={abstention:.1%}"
        )
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
