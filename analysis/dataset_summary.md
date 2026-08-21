# Dataset Summary

## Current Status

| Metric | Value |
| --- | ---: |
| Total instances | 9 |
| Upstream repositories | 5 |
| Languages | 3 |
| Conflict categories | 3 |
| Researcher-constructed instances | 9 |
| Reproduced instances | 9 |

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
| `zod__001` | `colinhacks/zod` | TypeScript | api_contract | researcher_constructed | reproduced |

## Notes

All current seed instances satisfy the AgentConflictBench acceptance rule:

1. Patch A passes independently.
2. Patch B passes independently.
3. Patch A and Patch B apply cleanly to the same base commit.
4. The composed patch pair fails a composition-level oracle.

The next target is another JavaScript/TypeScript library or a new conflict category such as security policy, dependency, or performance/resource behavior.
