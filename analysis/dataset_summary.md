# Dataset Summary

## Current Status

| Metric | Value |
| --- | ---: |
| Total instances | 4 |
| Upstream repositories | 2 |
| Languages | 1 |
| Conflict categories | 3 |
| Researcher-constructed instances | 4 |
| Reproduced instances | 4 |

## Instances

| ID | Repository | Language | Conflict Type | Source | Status |
| --- | --- | --- | --- | --- | --- |
| `click__001` | `pallets/click` | Python | configuration | researcher_constructed | reproduced |
| `click__002` | `pallets/click` | Python | behavioral | researcher_constructed | reproduced |
| `click__003` | `pallets/click` | Python | api_contract | researcher_constructed | reproduced |
| `typer__001` | `fastapi/typer` | Python | behavioral | researcher_constructed | reproduced |

## Notes

All current seed instances satisfy the AgentConflictBench acceptance rule:

1. Patch A passes independently.
2. Patch B passes independently.
3. Patch A and Patch B apply cleanly to the same base commit.
4. The composed patch pair fails a composition-level oracle.

The next targets are `typer__002` and the first TypeScript/JavaScript instance, preferably `commander__001`, so the benchmark demonstrates both cross-repository and cross-language applicability.
