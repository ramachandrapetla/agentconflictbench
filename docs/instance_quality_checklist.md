# Instance Quality Checklist

Use this checklist before marking an AgentConflictBench instance as
`reproduced`.

The goal is to keep the benchmark credible as it grows. A good instance should
feel like two plausible software-development tasks that are each correct alone
but unsafe when composed.

## Required Files

Each accepted instance must include:

- `metadata.json`
- `README.md`
- `task_a.md`
- `task_b.md`
- `patch_a.diff`
- `patch_b.diff`
- `combined.patch`
- `oracle/test_patch_a.*`
- `oracle/test_patch_b.*`
- `oracle/test_composition.*`
- `scripts/validate_a.sh`
- `scripts/validate_b.sh`
- `scripts/validate_composed.sh`
- `logs/validate_a.txt`
- `logs/validate_b.txt`
- `logs/validate_composed.txt`

## Acceptance Gate

An instance may be listed as `reproduced` only when all of these are true:

1. Patch A applies cleanly to the pinned base commit.
2. Patch B applies cleanly to the pinned base commit.
3. Patch A passes its independent oracle.
4. Patch B passes its independent oracle.
5. Patch A + Patch B apply cleanly together with no textual Git conflict.
6. The composed patch pair fails a composition-level oracle.
7. The composition failure disappears when either patch is removed.
8. The failure is caused by patch interaction, not setup, nondeterminism, or an
   unrelated upstream bug.

## Realism Gate

At least one of these should be true for each task:

- It resembles a plausible feature request, bug fix, refactor, default change,
  compatibility improvement, or hardening patch.
- It changes behavior that users, maintainers, or downstream code could
  reasonably depend on.
- It captures a mistake a coding agent could plausibly make while satisfying a
  local test.

Reject instances where either patch is merely contrived to fail when combined
and has no believable standalone purpose.

## Oracle Gate

Prefer automated oracles. A composition oracle should:

- assert the intended composed behavior directly;
- fail on A+B;
- pass on base+A;
- pass on base+B;
- avoid broad snapshots unless the snapshot is the behavior under study;
- avoid dependence on network services, wall-clock timing, or machine-specific
  paths.

## Metadata Gate

Run:

```bash
python scripts/validate_metadata.py
python scripts/check_instance_completeness.py
```

Check that:

- `base_commit` is a 40-character SHA;
- `repo`, `language`, `conflict_type`, `source`, and `status` match
  `instances/index.json`;
- referenced patch, oracle, and validation-script files exist;
- convention-based task files and `combined.patch` exist;
- `failure_summary` explains the interaction, not just the symptom.

## Documentation Boundaries

Keep the root README high-level. Do not add per-instance test logs or long
setup blocks there.

Use:

- `instances/<id>/README.md` for instance-specific explanation;
- `docs/reproduction.md` for upstream setup and reproduction commands;
- `analysis/dataset_summary.md` for generated dataset counts;
- `analysis/validation_report.md` for full-dataset validation results.

## Rejection Criteria

Reject or keep an instance as `candidate` if:

- either patch fails alone;
- the patches conflict textually;
- the composed failure is flaky;
- the oracle tests a behavior unrelated to the patch interaction;
- the task pair is unrealistic;
- setup requires private services, credentials, or unusually heavy
  infrastructure;
- the instance cannot be reproduced from a fresh clone and pinned metadata.

## Review Notes

Before merging a new instance, record:

- the upstream checkout path used for validation;
- the exact validation command;
- whether full-dataset validation passed;
- any setup caveats added to `docs/reproduction.md`.
