# Control Instance Design

AgentConflictBench is currently a positive-conflict benchmark: each reproduced
instance is expected to pass Patch A alone, pass Patch B alone, and fail under
the clean A+B composition. Control instances should add matched negative
examples where two independent changes compose cleanly and the composition
oracle passes.

## Purpose

Controls make the benchmark harder to game and easier to evaluate:

- They prevent a detector from scoring well by predicting conflict for every
  pair.
- They provide calibration examples for methods that produce confidence scores.
- They support paper claims about precision, not only recall on known conflicts.

## Canonical Layout

Control instances should use the same file shape as conflict instances:

- `task_a.md`
- `task_b.md`
- `patch_a.patch`
- `patch_b.patch`
- `combined.patch`
- `oracle/`
- `scripts/`
- `logs/`
- `metadata.json`
- `README.md`

The key semantic difference is the composition expectation:

- Conflict instance: Patch A passes, Patch B passes, A+B composition fails.
- Control instance: Patch A passes, Patch B passes, A+B composition passes.

## Metadata

All instances use one canonical metadata schema. The `composition_expected`
field declares whether the composition oracle should pass or fail:

```json
"composition_expected": "fail"
```

Allowed values should be:

- `fail`: a positive AgentConflictBench conflict instance.
- `pass`: a control instance with clean semantic composition.

This is cleaner than maintaining a separate control schema because all artifacts
and validation logic remain shared. Existing conflict instances use
`composition_expected = "fail"`; future controls should use
`composition_expected = "pass"`.

## Selection Criteria

A control should be matched to a conflict instance or repository slice on:

- same upstream repository and base commit where practical;
- similar patch size;
- similar touched-file count;
- similar task-description specificity;
- independent task intents;
- clean textual composition;
- passing composition oracle.

## Initial Control Targets

Prioritize JS/TS controls next because the positive set has just expanded in
that direction:

1. Commander.js: independent option-formatting and help-text behavior.
2. Commander.js: independent argument-description and error-message behavior.
3. Zod: independent metadata and string-format checks.
4. Zod: independent object-mode and array-size checks that do not share helper
   semantics.

## Validation Policy

The reproduction runner accepts both outcomes:

- `composition_expected = "fail"`: expect composition oracle failure.
- `composition_expected = "pass"`: expect composition oracle success.

Controls should be matched and documented with the same care as conflict
instances so they do not become trivial negatives.
