# Reproduction Guide

This guide keeps repository-specific setup out of the top-level README.

AgentConflictBench instances are reproduced against local clones of upstream
projects. Each instance pins its upstream base commit in `metadata.json`; the
runner checks out that commit, applies Patch A, applies Patch B, and then
checks the composed behavior.

## Reproduce One Instance

```bash
python scripts/run_instance.py instances/click__001 --repo-dir /tmp/click
```

A successful run means:

1. Patch A passes independently.
2. Patch B passes independently.
3. Patch A + Patch B apply without a textual Git conflict.
4. The composition oracle fails as expected.

## Upstream Setup

### Click

```bash
git clone https://github.com/pallets/click.git /tmp/click
cd /tmp/click
python -m pip install -e . pytest
```

Instances:

```bash
python scripts/run_instance.py instances/click__001 --repo-dir /tmp/click
python scripts/run_instance.py instances/click__002 --repo-dir /tmp/click
python scripts/run_instance.py instances/click__003 --repo-dir /tmp/click
python scripts/run_instance.py instances/click__004 --repo-dir /tmp/click
```

### Typer

```bash
git clone https://github.com/fastapi/typer.git /tmp/typer
cd /tmp/typer
python -m pip install -e . pytest rich shellingham
```

Instances:

```bash
python scripts/run_instance.py instances/typer__001 --repo-dir /tmp/typer
python scripts/run_instance.py instances/typer__002 --repo-dir /tmp/typer
```

### Commander.js

```bash
git clone https://github.com/tj/commander.js.git /tmp/commander
cd /tmp/commander
```

Instances:

```bash
python scripts/run_instance.py instances/commander__001 --repo-dir /tmp/commander
python scripts/run_instance.py instances/commander__002 --repo-dir /tmp/commander
```

### HTTPX

```bash
git clone https://github.com/encode/httpx.git /tmp/httpx
cd /tmp/httpx
python -m pip install -e . pytest
```

Instances:

```bash
python scripts/run_instance.py instances/httpx__001 --repo-dir /tmp/httpx
python scripts/run_instance.py instances/httpx__002 --repo-dir /tmp/httpx
```

### Zod

```bash
git clone https://github.com/colinhacks/zod.git /tmp/zod
cd /tmp/zod
npx pnpm@10.12.1 install --frozen-lockfile
```

Instances:

```bash
python scripts/run_instance.py instances/zod__001 --repo-dir /tmp/zod
```

## Validate The Dataset

Use `scripts/validate_dataset.py` to run every reproduced instance listed in
`instances/index.json` and write `analysis/validation_report.md`.

```bash
python scripts/validate_dataset.py \
  --repo click=/tmp/click \
  --repo typer=/tmp/typer \
  --repo commander.js=/tmp/commander \
  --repo httpx=/tmp/httpx \
  --repo zod=/tmp/zod
```

If each upstream checkout has its own virtual environment, pass the Python
executable for each repo:

```bash
python scripts/validate_dataset.py \
  --repo click=/tmp/click \
  --repo typer=/tmp/typer \
  --repo commander.js=/tmp/commander \
  --repo httpx=/tmp/httpx \
  --repo zod=/tmp/zod \
  --python click=/tmp/click/.venv/bin/python \
  --python typer=/tmp/typer/.venv/bin/python \
  --python httpx=/tmp/httpx/.venv/bin/python
```

Repository keys may be the repo name (`click`), owner/name (`pallets/click`),
or full GitHub URL.

## Bootstrap Upstream Repositories

Use `scripts/bootstrap_repos.py` to clone all upstream repositories referenced
by `instances/index.json` into a standard directory.

```bash
python scripts/bootstrap_repos.py --target-dir /tmp/agentconflictbench-repos --print-installs
```

The script clones repositories only. It prints dependency-installation notes so
reviewers can choose virtual environments and package managers explicitly.
