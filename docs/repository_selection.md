# Repository Selection

AgentConflictBench repository selection is based on whether a project can produce realistic, reproducible examples of silent semantic patch interference.

The goal is not to choose the most popular repositories. The goal is to choose repositories where independent AI-generated patches can plausibly pass alone, merge cleanly, and fail only when composed.

## Selection Criteria

Each candidate repository is scored from 1 to 5 on the following dimensions.

| Criterion | What We Check | Why It Matters |
| --- | --- | --- |
| Testability | Clear local test command, targeted tests possible, stable CI-style checks. | Every benchmark instance needs reproducible independent and composed validation. |
| Setup Cost | Can install and run tests without heavy services or long builds. | Expensive setup slows instance creation and makes reproduction harder. |
| Semantic Interaction Surface | Has APIs, config, schemas, defaults, state, protocols, or parser behavior likely to interact across patches. | Silent semantic interference needs meaningful composition behavior. |
| Task Realism | Has plausible standalone maintenance, feature, bug-fix, or behavior-change tasks. | Reviewers should believe these are tasks developers or coding agents would attempt. |
| Patch Granularity | Supports small-to-medium changes rather than only large architectural edits. | Benchmark instances should be understandable and auditable. |
| License and Redistribution | Permissive license and public source. | The benchmark may redistribute patches, metadata, and reproduction scripts. |
| Activity and Relevance | Active or widely used project with current ecosystem relevance. | Improves publication credibility and citation value. |

## Repository Fit Gate

A repository is accepted into the first benchmark wave only if it passes this pilot gate:

1. Clone the repository at a pinned commit.
2. Install dependencies in a fresh environment.
3. Run a small targeted test subset successfully.
4. Identify at least three plausible independent task pairs.
5. Create or generate at least one candidate patch pair.
6. Verify Patch A passes independently.
7. Verify Patch B passes independently.
8. Verify Patch A + Patch B merge without textual conflict.
9. Verify the composed version fails a specific oracle.
10. Verify the failure disappears when either patch is removed.

The pilot gate is how we make sure a repository fits the benchmark, instead of assuming fit from popularity.

## First-Pass Candidate Scoring

| Repository | Language | Testability | Setup Cost | Semantic Surface | Task Realism | Patch Granularity | License | Activity/Relevance | Decision |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- |
| pallets/click | Python | 5 | 5 | 5 | 5 | 5 | BSD-3-Clause | 5 | Primary |
| fastapi/typer | Python | 4 | 4 | 5 | 5 | 4 | MIT | 5 | Primary |
| encode/httpx | Python | 5 | 4 | 5 | 5 | 4 | BSD-3-Clause | 5 | Primary |
| pallets/markupsafe | Python | 5 | 5 | 5 | 5 | 5 | BSD-3-Clause | 5 | Primary |
| Textualize/rich | Python | 5 | 5 | 5 | 5 | 5 | MIT | 5 | Primary |
| colinhacks/zod | TypeScript | 5 | 4 | 5 | 5 | 4 | MIT | 5 | Primary |
| tj/commander.js | TypeScript/JavaScript | 5 | 5 | 5 | 5 | 5 | MIT | 5 | Primary |
| pydantic/pydantic | Python | 5 | 2 | 5 | 5 | 3 | MIT | 5 | Alternate |
| dotenvx/dotenvx | JavaScript | 4 | 3 | 5 | 5 | 4 | BSD-3-Clause | 4 | Alternate |
| sindresorhus/meow | TypeScript/JavaScript | 4 | 4 | 4 | 4 | 5 | MIT | 4 | Alternate |

## Recommended Seed Repositories

### 1. pallets/click

Click is a Python command-line interface toolkit. It is a strong fit because CLI parsing has many semantic interaction points: option defaults, aliases, env vars, command nesting, help generation, shell completion, prompting, and error behavior. These are ideal for patches that pass alone but conflict when combined.

Example conflict directions:

- Patch A changes option precedence while Patch B adds an option relying on old precedence.
- Patch A changes help formatting while Patch B adds command-group behavior that assumes old wrapping rules.
- Patch A changes environment-variable handling while Patch B adds prompt fallback behavior.

### 2. fastapi/typer

Typer builds CLIs from Python type hints. It is useful because semantic behavior emerges from type annotations, defaults, command inference, rich output, completion, and Click compatibility. It is close enough to Click to produce related examples but different enough to broaden the benchmark.

Example conflict directions:

- Patch A changes annotation parsing while Patch B adds support for a new parameter type.
- Patch A changes rich help rendering while Patch B changes default command behavior.
- Patch A changes callback invocation while Patch B changes nested command handling.

### 3. encode/httpx

HTTPX is a Python HTTP client. It has strong composition surfaces: timeout behavior, redirects, cookies, headers, authentication, proxies, transports, async/sync APIs, and protocol handling. Many failures are behavioral rather than textual.

Example conflict directions:

- Patch A changes redirect header handling while Patch B changes authentication propagation.
- Patch A changes timeout defaults while Patch B changes streaming behavior.
- Patch A changes proxy selection while Patch B changes environment-variable behavior.

### 4. colinhacks/zod

Zod is a TypeScript schema validation library. It is strong for API-contract, schema, inference, default, transform, and error-format conflicts. TypeScript also lets us test both runtime behavior and type-level expectations.

Example conflict directions:

- Patch A changes optional/default semantics while Patch B changes object merge behavior.
- Patch A changes error formatting while Patch B adds a validator relying on previous issue paths.
- Patch A changes transform ordering while Patch B changes refinement behavior.

### 5. tj/commander.js

Commander is a Node.js command-line parser. It has small setup, a clear test command, and many semantic interaction points: option parsing, aliases, commands, argument validation, help output, env/default behavior, and TypeScript definitions.

Example conflict directions:

- Patch A changes negated boolean option handling while Patch B adds default-value behavior.
- Patch A changes subcommand parsing while Patch B changes unknown-option handling.
- Patch A changes TypeScript typings while Patch B changes runtime API behavior.

### 6. Textualize/rich

Rich is a Python terminal-rendering library. It is a strong expansion fit
because rendering behavior depends on text spans, markup, padding, console
options, emoji handling, wrapping, measurement, and metadata propagation. These
surfaces produce compact, realistic semantic interactions with low setup cost.

Example conflict directions:

- Patch A changes styled text padding while Patch B refactors truncation to use
  the padding helper.
- Patch A changes low-level text metadata inheritance while Patch B delegates a
  public API to that helper.
- Patch A changes markup escaping while Patch B changes emoji or tag parsing.

### 7. pallets/markupsafe

MarkupSafe is a Python HTML-safe string library. It is a strong fit because it
has compact code, low setup cost, and subtle protocol contracts around
escaping, `Markup` construction, old-style formatting, new-style formatting,
bytes conversion, and `__html__` / `__html_format__` precedence.

Example conflict directions:

- Patch A changes optional-value handling in one formatting helper while Patch
  B reuses that helper from another formatting path.
- Patch A changes byte-string conversion while Patch B delegates escaping
  through the conversion helper.
- Patch A changes HTML protocol precedence while Patch B centralizes
  constructor behavior through the escape helper.

## Why These Fit AgentConflictBench

These repositories share the properties we need:

1. They have realistic developer-facing behavior with many implicit contracts.
2. They have clear tests and manageable local validation paths.
3. They allow small patches that are easy to inspect.
4. They are popular enough that benchmark examples feel meaningful.
5. They expose semantic interactions that Git cannot detect textually.

## Initial Seed Plan

Start with two seed instances per primary repository, then expand with
additional repositories that pass the pilot gate:

| Repository | Seed Instances | Target Conflict Categories |
| --- | ---: | --- |
| pallets/click | 2 | configuration, behavioral |
| fastapi/typer | 2 | API-contract, behavioral |
| encode/httpx | 2 | behavioral, security-policy |
| pallets/markupsafe | 3 | API-contract, test-assumption |
| Textualize/rich | 2 | behavioral, API-contract |
| colinhacks/zod | 2 | schema, API-contract |
| tj/commander.js | 2 | configuration, test-assumption |

The initial five-repository plan provided 10 target instances. The current seed
dataset has expanded to 20 reproduced instances across 7 repositories while
preserving the same inclusion gate.

## Validation Before Inclusion

No repository is permanently included until the first seed instance passes the full AgentConflictBench quality-control checklist. If a repo proves too slow, flaky, or difficult to reproduce, it moves to the alternate list.
