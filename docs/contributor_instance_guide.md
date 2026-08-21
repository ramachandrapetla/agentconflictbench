# Contributor Instance Guide

This guide explains how to add benchmark instances that are useful for research
and easy for reviewers to reproduce.

## 1. Choose a Good Candidate

Good AgentConflictBench instances have two independent development intents that
look reasonable in isolation.

For positive conflict instances, the two patches should interact through a
hidden contract such as:

- configuration precedence;
- API contract assumptions;
- state invariants;
- security policy;
- validation semantics;
- test assumptions;
- performance or resource behavior.

For control instances, the two patches should be similarly sized and realistic
but semantically independent enough that the composition oracle passes.

## 2. Pin the Base Commit

Every instance must target a specific upstream commit. Use a full 40-character
SHA in `metadata.json`.

The benchmark should be reproducible from:

```bash
git checkout --detach <base_commit>
git apply patch_a.patch
```

and similarly for Patch B and the composed patch pair.

## 3. Write Agent-Readable Tasks

Use:

- `task_a.md` for Patch A's standalone intent;
- `task_b.md` for Patch B's standalone intent.

Each task should be concise but specific enough that an agent could implement
it without seeing the reference patch. Include constraints such as "do not
change parsing behavior" or "preserve existing validation semantics" when they
matter.

## 4. Add Reference Patches

Use:

- `patch_a.patch`
- `patch_b.patch`
- `combined.patch`

`combined.patch` should represent Patch A and Patch B applied together cleanly
to the pinned base commit.

## 5. Add Oracles

Each instance needs:

- `oracle/test_patch_a.*`
- `oracle/test_patch_b.*`
- `oracle/test_composition.*`

Patch A and Patch B oracles should pass independently. The composition oracle
should match `composition_expected`:

- positive conflict: composition oracle fails;
- control: composition oracle passes.

## 6. Add Validation Scripts and Logs

Each instance needs:

- `scripts/validate_a.sh`
- `scripts/validate_b.sh`
- `scripts/validate_composed.sh`
- `logs/validate_a.txt`
- `logs/validate_b.txt`
- `logs/validate_composed.txt`

Logs should preserve useful pass/fail evidence but avoid local absolute paths.
Use placeholders such as `<agentconflictbench>` and `<upstream-checkout>` if
needed.

## 7. Update Metadata and Index

Add `metadata.json` and update `instances/index.json`.

Recommended metadata values:

- `source`: `researcher_constructed` unless the instance was mined or hybrid;
- `merge_result`: explain that the patches apply cleanly with `git apply`;
- `failure_summary`: for controls, summarize why composition is expected to
  pass; for conflicts, summarize why composition fails.

## 8. Validate

Run:

```bash
python scripts/validate_metadata.py
python scripts/check_instance_completeness.py
python scripts/run_instance.py instances/<instance_id> --repo-dir /path/to/upstream
python scripts/validate_generated_artifacts.py
python scripts/validate_public_artifacts.py
```

If generated files changed, commit them with the instance.

## 9. Open a Pull Request

In the PR body, include:

- the upstream repository and base commit;
- whether the instance is a positive conflict or control;
- the hidden contract or independence rationale;
- validation commands and results.
