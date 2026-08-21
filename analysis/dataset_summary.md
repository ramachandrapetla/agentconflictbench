# Dataset Summary

## Current Status

| Metric | Value |
| --- | ---: |
| Total instances | 8 |
| Upstream repositories | 4 |
| Languages | 2 |
| Conflict categories | 3 |
| Researcher-constructed instances | 8 |
| Reproduced instances | 8 |

## Instances

| ID | Repository | Language | Conflict Type | Source | Status |
| --- | --- | --- | --- | --- | --- |
| `click__001` | `pallets/click` | Python | configuration | researcher_constructed | reproduced |
| `click__002` | `pallets/click` | Python | behavioral | researcher_constructed | reproduced |
| `click__003` | `pallets/click` | Python | api_contract | researcher_constructed | reproduced |
| `click__004` | `pallets/click` | Python | behavioral | researcher_constructed | reproduced |
| `typer__001` | `fastapi/typer` | Python | behavioral | researcher_constructed | reproduced |
| `typer__002` | `fastapi/typer` | Python | behavioral | researcher_constructed | reproduced |
| `commander__001` | `tj/commander.js` | JavaScript | behavioral | researcher_constructed | reproduced |
| `httpx__001` | `encode/httpx` | Python | api_contract | researcher_constructed | reproduced |

## Notes

All current seed instances satisfy the AgentConflictBench acceptance rule:

1. Patch A passes independently.
2. Patch B passes independently.
3. Patch A and Patch B apply cleanly to the same base commit.
4. The composed patch pair fails a composition-level oracle.

The next target is a schema/API-contract instance from `colinhacks/zod` or another JavaScript/TypeScript library, so the benchmark continues broadening beyond Python-heavy CLI and HTTP-client cases.
