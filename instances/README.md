# Benchmark Instances

This directory contains AgentConflictBench instances.

## Canonical Instance Layout

Each accepted instance uses this layout:

```text
instances/<instance_id>/
  task_a.md
  task_b.md
  patch_a.patch
  patch_b.patch
  combined.patch
  oracle/
    test_patch_a.*
    test_patch_b.*
    test_composition.*
  scripts/
    validate_a.sh
    validate_b.sh
    validate_composed.sh
  logs/
    validate_a.txt
    validate_b.txt
    validate_composed.txt
  metadata.json
  README.md
```

`task_a.md` and `task_b.md` describe the independent development intents.
`patch_a.patch` and `patch_b.patch` are the reference implementations for those
tasks. `combined.patch` is the clean textual composition of Patch A and Patch B
from the pinned base commit.

The task files are convention-based rather than referenced from metadata. This
keeps the instance shape stable and avoids duplicating canonical filenames in
`metadata.json`.

An instance is accepted only when both patches pass independently, merge without textual Git conflict, and fail a composition-level oracle when combined.
