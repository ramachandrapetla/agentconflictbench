#!/usr/bin/env python3
"""Evaluate simple oracle-free baselines for conflict/control prediction."""

from __future__ import annotations

import argparse
import csv
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class InstanceRow:
    instance_id: str
    repo: str
    language: str
    conflict_type: str
    composition_expected: str
    same_file: int
    shared_files: int
    patch_total_lines: int
    changed_token_jaccard: float
    task_token_jaccard: float

    @property
    def label(self) -> int:
        return 1 if self.composition_expected == "fail" else 0


@dataclass(frozen=True)
class Baseline:
    name: str
    description: str
    score: Callable[[InstanceRow], float]
    threshold: float


@dataclass(frozen=True)
class Metrics:
    tp: int
    fp: int
    tn: int
    fn: int
    accuracy: float
    precision: float
    recall: float
    specificity: float
    f1: float
    balanced_accuracy: float
    roc_auc: float | None


def parse_int(row: dict[str, str], field: str) -> int:
    return int(row[field])


def parse_float(row: dict[str, str], field: str) -> float:
    return float(row[field])


def load_rows(path: Path) -> list[InstanceRow]:
    rows: list[InstanceRow] = []
    with path.open(newline="") as csv_file:
        for row in csv.DictReader(csv_file):
            patch_total_lines = sum(
                parse_int(row, field)
                for field in [
                    "patch_a_added_lines",
                    "patch_a_deleted_lines",
                    "patch_b_added_lines",
                    "patch_b_deleted_lines",
                ]
            )
            rows.append(
                InstanceRow(
                    instance_id=row["id"],
                    repo=row["repo"],
                    language=row["language"],
                    conflict_type=row["conflict_type"],
                    composition_expected=row["composition_expected"],
                    same_file=parse_int(row, "same_file"),
                    shared_files=parse_int(row, "shared_files"),
                    patch_total_lines=patch_total_lines,
                    changed_token_jaccard=parse_float(row, "changed_token_jaccard"),
                    task_token_jaccard=parse_float(row, "task_token_jaccard"),
                )
            )

    if not rows:
        raise SystemExit(f"No feature rows found: {path}")

    return rows


def safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def roc_auc(labels: list[int], scores: list[float]) -> float | None:
    positive_scores = [score for label, score in zip(labels, scores) if label == 1]
    negative_scores = [score for label, score in zip(labels, scores) if label == 0]

    if not positive_scores or not negative_scores:
        return None

    wins = 0.0
    comparisons = 0
    for positive_score in positive_scores:
        for negative_score in negative_scores:
            comparisons += 1
            if positive_score > negative_score:
                wins += 1.0
            elif positive_score == negative_score:
                wins += 0.5

    return wins / comparisons


def evaluate(rows: list[InstanceRow], baseline: Baseline) -> Metrics:
    labels = [row.label for row in rows]
    scores = [baseline.score(row) for row in rows]
    predictions = [1 if score >= baseline.threshold else 0 for score in scores]

    tp = sum(1 for label, pred in zip(labels, predictions) if label == 1 and pred == 1)
    fp = sum(1 for label, pred in zip(labels, predictions) if label == 0 and pred == 1)
    tn = sum(1 for label, pred in zip(labels, predictions) if label == 0 and pred == 0)
    fn = sum(1 for label, pred in zip(labels, predictions) if label == 1 and pred == 0)

    accuracy = safe_div(tp + tn, len(rows))
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    specificity = safe_div(tn, tn + fp)
    f1 = safe_div(2 * precision * recall, precision + recall)
    balanced_accuracy = (recall + specificity) / 2

    return Metrics(
        tp=tp,
        fp=fp,
        tn=tn,
        fn=fn,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        specificity=specificity,
        f1=f1,
        balanced_accuracy=balanced_accuracy,
        roc_auc=roc_auc(labels, scores),
    )


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def fmt(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.3f}"


def render_report(rows: list[InstanceRow], baselines: list[Baseline]) -> str:
    positives = sum(row.label for row in rows)
    controls = len(rows) - positives
    metrics_by_name = [(baseline, evaluate(rows, baseline)) for baseline in baselines]

    metric_rows = []
    for baseline, metrics in metrics_by_name:
        metric_rows.append(
            [
                baseline.name,
                fmt(metrics.accuracy),
                fmt(metrics.precision),
                fmt(metrics.recall),
                fmt(metrics.specificity),
                fmt(metrics.f1),
                fmt(metrics.balanced_accuracy),
                fmt(metrics.roc_auc),
                f"{metrics.tp}/{metrics.fp}/{metrics.tn}/{metrics.fn}",
            ]
        )

    description_rows = [
        [baseline.name, baseline.description, f"{baseline.threshold:.3f}"]
        for baseline in baselines
    ]

    lines = [
        "# Baseline Classifier Results",
        "",
        "<!-- Generated by scripts/baseline_classifier.py. Do not edit by hand. -->",
        "",
        "This report evaluates simple oracle-free heuristics for predicting whether",
        "a patch pair is a positive silent semantic conflict (`composition_expected = fail`)",
        "or a clean-composition control (`composition_expected = pass`).",
        "",
        "## Dataset",
        "",
        *markdown_table(
            ["Metric", "Value"],
            [
                ["Instances", str(len(rows))],
                ["Positive conflicts", str(positives)],
                ["Controls", str(controls)],
                ["Control ratio", fmt(safe_div(controls, len(rows)))],
            ],
        ),
        "",
        "## Baselines",
        "",
        *markdown_table(["Baseline", "Rule", "Threshold"], description_rows),
        "",
        "## Metrics",
        "",
        *markdown_table(
            [
                "Baseline",
                "Accuracy",
                "Precision",
                "Recall",
                "Specificity",
                "F1",
                "Balanced Acc.",
                "ROC-AUC",
                "TP/FP/TN/FN",
            ],
            metric_rows,
        ),
        "",
        "## Interpretation",
        "",
        "These results are preliminary because the current seed dataset has only",
        f"{controls} controls. The most important numbers at this stage are specificity",
        "and balanced accuracy: they show whether a heuristic can avoid predicting",
        "conflict for every patch pair.",
        "",
        "The `always_conflict` baseline is intentionally included as a sanity check.",
        "It has perfect recall on positive conflicts but zero specificity on controls.",
        "",
    ]

    return "\n".join(lines)


def build_baselines(rows: list[InstanceRow]) -> list[Baseline]:
    patch_sizes = [row.patch_total_lines for row in rows]
    median_patch_size = statistics.median(patch_sizes)

    return [
        Baseline(
            name="always_conflict",
            description="Predict every patch pair is a conflict.",
            score=lambda row: 1.0,
            threshold=0.5,
        ),
        Baseline(
            name="same_file",
            description="Predict conflict when Patch A and Patch B touch at least one shared file.",
            score=lambda row: float(row.same_file),
            threshold=0.5,
        ),
        Baseline(
            name="changed_token_jaccard_ge_0.25",
            description="Predict conflict when changed-token Jaccard similarity is at least 0.25.",
            score=lambda row: row.changed_token_jaccard,
            threshold=0.25,
        ),
        Baseline(
            name="task_token_jaccard_ge_0.30",
            description="Predict conflict when task-description token Jaccard similarity is at least 0.30.",
            score=lambda row: row.task_token_jaccard,
            threshold=0.30,
        ),
        Baseline(
            name="patch_size_ge_median",
            description="Predict conflict when total changed lines are at least the dataset median.",
            score=lambda row: float(row.patch_total_lines),
            threshold=float(median_patch_size),
        ),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--features",
        type=Path,
        default=ROOT / "analysis" / "baseline_features.csv",
        help="Input CSV produced by scripts/baseline_features.py.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "analysis" / "baseline_classifier_results.md",
        help="Markdown report output path.",
    )
    args = parser.parse_args()

    rows = load_rows(args.features)
    report = render_report(rows, build_baselines(rows))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report)
    print(f"Wrote baseline classifier report to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
