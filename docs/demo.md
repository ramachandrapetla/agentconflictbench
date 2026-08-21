# Demo: One Silent Semantic Conflict

This walkthrough shows the benchmark pattern using `click__001`.

`click__001` contains two independently valid changes to Click option default
resolution:

- Patch A lets `default_map` accept dashed option names such as `api-key`.
- Patch B gives `default_map` higher precedence than automatically derived
  environment variables.

Each patch passes alone. The patches also apply together without a textual Git
conflict. But when composed, a command that previously preferred
`APP_API_KEY=from-env` now returns `from-map` because the two precedence changes
interact.

## Run the Instance

Clone Click and check out the pinned commit:

```bash
git clone https://github.com/pallets/click /tmp/click
git -C /tmp/click checkout --detach 2c8cd3ac958a7eb316d67f2d316c27086c4c0369
```

Install the Python test dependencies needed for your local environment. Then
run:

```bash
python scripts/run_instance.py instances/click__001 --repo-dir /tmp/click
```

The runner performs three checks:

1. Apply Patch A and run `oracle/test_patch_a.py`.
2. Restore, apply Patch B, and run `oracle/test_patch_b.py`.
3. Restore, apply both patches, and run `oracle/test_composition.py`.

For this positive conflict instance, the third oracle is expected to fail. The
runner reports PASS when the observed behavior matches the metadata label:

```text
PASS: instance reproduces expected silent semantic conflict.
```

## Why This Matters

Traditional merge tooling catches textual conflicts. Unit tests for isolated
tasks can catch broken individual patches. AgentConflictBench targets the gap
between those two checks: independently valid patches that merge cleanly but
violate a shared semantic assumption when composed.
