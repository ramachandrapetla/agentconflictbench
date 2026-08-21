# Rejected Candidate Log

This log records candidate ideas that were rejected, held, or revised before
becoming AgentConflictBench instances.

The purpose is methodological: as the dataset grows, we want to avoid inflating
counts with near-duplicates or weakly realistic examples. A rejected candidate
may still become useful later if it is revised to exercise a materially
different subsystem, hidden contract, or conflict type.

## Entry Format

Use this compact shape for future entries:

```text
## YYYY-MM-DD: <repo> / <candidate-name>

- Candidate idea:
- Decision: rejected | held | revised
- Reason:
- Near-duplicate of:
- Future use:
```

## 2026-08-21: encode/httpx / case-insensitive QueryParams get

- Candidate idea: combine a case-insensitive `QueryParams.__contains__` change
  with a `QueryParams.get()` refactor through the mapping protocol.
- Decision: rejected
- Reason: near-duplicate of the accepted HTTPX query-parameter interaction.
  It touched the same subsystem, same hidden contract, and same oracle shape.
- Near-duplicate of: `httpx__001`
- Future use: no, unless revised around a different HTTPX subsystem such as
  redirects, proxies, streaming, or cookie policy.

## 2026-08-21: tj/commander.js / repeated command alias lookup

- Candidate idea: add another clean-merge command-resolution conflict involving
  command prefix lookup and case-insensitive fallback.
- Decision: rejected
- Reason: near-duplicate of accepted Commander/Typer CLI command-resolution
  examples. It would overrepresent alias/prefix lookup conflicts.
- Near-duplicate of: `commander__001`, `typer__001`, `typer__002`
- Future use: no, unless it targets a different Commander contract such as help
  generation, option implication/conflict validation, or default precedence.

## 2026-08-21: colinhacks/zod / second metadata wrapper inheritance

- Candidate idea: create another Zod metadata-inheritance conflict around
  wrapper schemas.
- Decision: held
- Reason: promising TypeScript coverage, but too close to the accepted optional
  wrapper metadata/id conflict without a different schema subsystem.
- Near-duplicate of: `zod__001`
- Future use: yes, if revised around transforms, refinements, error paths,
  object merge behavior, or type-level expectations.
