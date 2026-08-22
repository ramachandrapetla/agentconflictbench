# Artifact Review Checklist

This checklist is for researchers, reviewers, and contributors who want to
quickly evaluate whether AgentConflictBench is complete enough to inspect,
reuse, or cite.

## 1. Start With the Dataset Snapshot

Read:

- [`analysis/dataset_summary.md`](../analysis/dataset_summary.md)
- [`analysis/validation_report.md`](../analysis/validation_report.md)
- [`paper/dataset_table.md`](../paper/dataset_table.md)

The current seed dataset contains 28 reproduced instances: 25 positive
conflict instances and 3 clean-composition controls.

## 2. Inspect the Instance Shape

Every reproduced instance should have:

```text
task_a.md
task_b.md
patch_a.patch
patch_b.patch
combined.patch
oracle/
scripts/
logs/
metadata.json
README.md
```

See [`instances/README.md`](../instances/README.md) for the canonical layout.

## 3. Run Static Repository Checks

From the repository root:

```bash
python scripts/validate_metadata.py
python scripts/check_instance_completeness.py
python scripts/validate_generated_artifacts.py
python scripts/validate_public_artifacts.py
```

These checks do not reproduce every upstream project, but they verify metadata,
instance shape, generated summaries, and public-release hygiene.

## 4. Run One Instance

Use the demo path first:

```bash
python scripts/run_instance.py instances/click__001 --repo-dir /tmp/click
```

For setup details, use [`docs/demo.md`](demo.md) and
[`docs/reproduction.md`](reproduction.md).

The runner reports PASS when the observed composition behavior matches
`composition_expected`.

## 5. Interpret Positive Conflicts vs Controls

Positive conflict instance:

- Patch A passes alone.
- Patch B passes alone.
- Patch A + Patch B applies cleanly.
- The composition oracle fails.
- `composition_expected = "fail"`.

Control instance:

- Patch A passes alone.
- Patch B passes alone.
- Patch A + Patch B applies cleanly.
- The composition oracle passes.
- `composition_expected = "pass"`.
- `conflict_type = "control"`.

## 6. Check Known Limitations

The current seed dataset is intentionally small. The main limitations are:

- only 3 controls so far;
- Python and JavaScript/TypeScript are prioritized first;
- dependency and performance/resource categories are not yet represented;
- full-dataset reproduction still requires per-repository dependency setup.

Open issues track these next steps.

## 7. What Makes the Artifact Useful

AgentConflictBench is useful when an instance demonstrates a real composition
risk that isolated task validation misses:

1. each patch appears valid alone;
2. Git reports no textual conflict;
3. the composed behavior violates a shared semantic assumption.

That makes the benchmark complementary to single-task coding-agent benchmarks.
