# click__001: Dashed default_map alias vs. auto envvar precedence

This is the first seeded AgentConflictBench instance.

## Repository

- Upstream: https://github.com/pallets/click
- Base commit: `2c8cd3ac958a7eb316d67f2d316c27086c4c0369`
- Language: Python
- Conflict type: configuration
- Source: researcher_constructed

## Task A

Allow `Context.default_map` to use dashed option names, such as `api-key`, as aliases for Click's internal underscored parameter names, such as `api_key`.

Patch A passes its validation oracle.

## Task B

Allow `Context.default_map` values to override automatically derived environment variable values during option resolution.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, a dashed `default_map` alias unexpectedly overrides an auto envvar value.

The composition oracle constructs this command:

```python
@click.command()
@click.option("--api-key")
def cli(api_key):
    click.echo(api_key)
```

It invokes the command with:

```python
auto_envvar_prefix="APP"
default_map={"api-key": "from-map"}
env={"APP_API_KEY": "from-env"}
```

The expected composed output is:

```text
from-env
```

The actual composed output after applying Patch A + Patch B is:

```text
from-map
```

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from interaction between two independently plausible configuration-precedence changes.

## Files

- `patch_a.patch`: dashed `default_map` alias support.
- `patch_b.patch`: default-map-before-auto-envvar precedence change.
- `oracle/test_patch_a.py`: Patch A validation oracle.
- `oracle/test_patch_b.py`: Patch B validation oracle.
- `oracle/test_composition.py`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
