# Publishing AgentConflictBench on Hugging Face

This guide explains how to create a Hugging Face Dataset package from the
GitHub repository.

GitHub remains the development source of truth. Hugging Face should host a
dataset-friendly snapshot that people can discover, preview, and load with
`datasets`.

## Build the Upload Folder

From the repository root:

```bash
python scripts/export_huggingface_dataset.py \
  --clean \
  --output dist/huggingface \
  --repo-id ramachandra1996/agentconflictbench
```

This creates:

```text
dist/huggingface/
  README.md
  LICENSE
  CITATION.cff
  data/
    instances.jsonl
    instances.csv
  artifacts/
    instances.zip
```

`data/instances.jsonl` is the primary Hugging Face data file. Each row contains
one benchmark instance with task descriptions, patches, oracles, metadata, and
composition labels.

`artifacts/instances.zip` contains the canonical instance folders for users who
want the exact task/patch/oracle/script/log layout.

## Create the Hugging Face Dataset Repo

Create a Dataset repository on Hugging Face named:

```text
ramachandra1996/agentconflictbench
```

Use the `dataset` repo type, not `model` or `space`.

## Upload

Install the Hub client and log in:

```bash
pip install huggingface_hub
huggingface-cli login
```

Then upload the generated folder:

```bash
python - <<'PY'
from huggingface_hub import HfApi

api = HfApi()
api.upload_folder(
    folder_path="dist/huggingface",
    repo_id="ramachandra1996/agentconflictbench",
    repo_type="dataset",
)
PY
```

The Hugging Face Hub will render `dist/huggingface/README.md` as the dataset
card.

## Load the Dataset

After upload:

```python
from datasets import load_dataset

dataset = load_dataset("ramachandra1996/agentconflictbench")
print(dataset["train"][0]["id"])
```

## Recommended Release Rhythm

Use GitHub for day-to-day development. Publish a new Hugging Face snapshot
after meaningful dataset milestones, for example:

- first public seed dataset;
- 50 instances;
- 100 instances;
- paper submission artifact;
- camera-ready artifact.

Before each upload, run:

```bash
python scripts/validate_metadata.py
python scripts/check_instance_completeness.py
python scripts/validate_generated_artifacts.py
python scripts/validate_public_artifacts.py
python scripts/export_huggingface_dataset.py \
  --clean \
  --output dist/huggingface \
  --repo-id ramachandra1996/agentconflictbench
```

## Notes

- Do not commit `dist/`; it is generated and ignored by Git.
- Keep large generated artifacts on Hugging Face, not in the GitHub repo.
- Keep the GitHub README concise and put Hugging Face-specific details here.
