# Control Instance Design

AgentConflictBench contains positive-conflict instances and clean-composition
controls. Positive instances pass Patch A alone, pass Patch B alone, and fail
under the clean A+B composition. Control instances are matched negative examples
where two independent changes compose cleanly and the composition oracle passes.

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
"composition_expected": "pass"
```

Allowed values should be:

- `fail`: a positive AgentConflictBench conflict instance.
- `pass`: a control instance with clean semantic composition.

This is cleaner than maintaining a separate control schema because all artifacts
and validation logic remain shared. Conflict instances use
`composition_expected = "fail"` and controls use
`composition_expected = "pass"` with `conflict_type = "control"`.

## Selection Criteria

A control should be matched to a conflict instance or repository slice on:

- same upstream repository and base commit where practical;
- similar patch size;
- similar touched-file count;
- similar task-description specificity;
- independent task intents;
- clean textual composition;
- passing composition oracle.

## Initial Controls

The first controls are deliberately matched to repositories already represented
in the positive set:

1. `commander_control__001`: independent argument and option introspection APIs.
2. `httpx_control__001`: independent header and query-parameter helpers.
3. `zod_control__001`: independent string-format and number-format helpers.

The next target is to expand this set to at least 10 controls while keeping
patch size, task specificity, and touched-file overlap comparable to the
positive set.

## Validation Policy

The reproduction runner accepts both outcomes:

- `composition_expected = "fail"`: expect composition oracle failure.
- `composition_expected = "pass"`: expect composition oracle success.

Controls should be matched and documented with the same care as conflict
instances so they do not become trivial negatives.
