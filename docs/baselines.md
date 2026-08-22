# Baseline Experiment Scaffolding

AgentConflictBench should report simple baselines before claiming that silent
semantic conflicts require deeper reasoning. The first baselines are deliberately
small and auditable.

## Implemented Feature Baselines

`scripts/baseline_features.py` extracts per-instance features from task files,
metadata, and patch artifacts:

- changed files in Patch A and Patch B;
- same-file overlap count;
- added/deleted line counts for each patch;
- changed-line Jaccard similarity;
- task-token Jaccard similarity;
- whether both patches touch exactly one file;
- whether both patches touch the same file.

These features support simple classifiers or ranking heuristics such as:

- same-file overlap predicts risk;
- high patch-line overlap predicts risk;
- high task-description similarity predicts risk;
- patch size predicts risk.

## Example

```bash
python scripts/baseline_features.py --output analysis/baseline_features.csv
```

The script does not run models or make statistical claims. It prepares the
feature table that later experiments can consume.

The current descriptive snapshot is summarized in
`analysis/baseline_results.md`.

## Classifier-Style Baselines

`scripts/baseline_classifier.py` evaluates simple oracle-free heuristics over
`analysis/baseline_features.csv`.

```bash
python scripts/baseline_classifier.py \
  --features analysis/baseline_features.csv \
  --output analysis/baseline_classifier_results.md
```

The current report is written to
`analysis/baseline_classifier_results.md`. These results are preliminary while
the control set is small, but they give the paper a concrete first experimental
baseline.

## Next Baselines

- touched-symbol overlap;
- AST-level touched-function overlap;
- oracle-free static review prompts;
- repository-test pass/fail deltas;
- positive-control clean compositions.
