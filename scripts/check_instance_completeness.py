#!/usr/bin/env python3
"""Check that reproduced benchmark instances follow the repository shape."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_ORACLE_SUFFIXES = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx"}
REQUIRED_LOGS = [
    "logs/validate_a.txt",
    "logs/validate_b.txt",
    "logs/validate_composed.txt",
]
REQUIRED_SCRIPTS = [
    "scripts/validate_a.sh",
    "scripts/validate_b.sh",
    "scripts/validate_composed.sh",
]


@dataclass(frozen=True)
class CompletenessError:
    instance_id: str
    message: str


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        raise SystemExit(f"Missing JSON file: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from None


def load_index(index_path: Path) -> list[dict[str, Any]]:
    data = load_json(index_path)
    instances = data.get("instances", [])
    if not isinstance(instances, list):
        raise SystemExit(f"Invalid index format: {index_path}")
    return [instance for instance in instances if isinstance(instance, dict)]


def require_file(
    errors: list[CompletenessError],
    instance_id: str,
    instance_dir: Path,
    relative_path: str,
) -> None:
    if not (instance_dir / relative_path).is_file():
        errors.append(
            CompletenessError(instance_id, f"missing required file: {relative_path}")
        )


def require_oracle(
    errors: list[CompletenessError],
    instance_id: str,
    instance_dir: Path,
    stem: str,
) -> None:
    matches = sorted((instance_dir / "oracle").glob(f"{stem}.*"))
    matches = [path for path in matches if path.suffix in ALLOWED_ORACLE_SUFFIXES]

    if not matches:
        errors.append(
            CompletenessError(
                instance_id,
                f"missing required oracle matching oracle/{stem}.*",
            )
        )
        return

    if len(matches) > 1:
        names = ", ".join(str(path.relative_to(instance_dir)) for path in matches)
        errors.append(
            CompletenessError(instance_id, f"ambiguous oracle files for {stem}: {names}")
        )


def check_metadata_references(
    errors: list[CompletenessError],
    instance_id: str,
    instance_dir: Path,
    metadata: dict[str, Any],
) -> None:
    expected = {
        "patch_a": "patch_a.patch",
        "patch_b": "patch_b.patch",
        "validation_a": "scripts/validate_a.sh",
        "validation_b": "scripts/validate_b.sh",
    }

    for field, expected_value in expected.items():
        if metadata.get(field) != expected_value:
            errors.append(
                CompletenessError(
                    instance_id,
                    f"metadata field {field} should be {expected_value!r}",
                )
            )

    composition_oracle = metadata.get("composition_oracle")
    if not isinstance(composition_oracle, str):
        errors.append(
            CompletenessError(instance_id, "metadata field composition_oracle must be a string")
        )
    elif not composition_oracle.startswith("oracle/test_composition."):
        errors.append(
            CompletenessError(
                instance_id,
                "metadata field composition_oracle should point to oracle/test_composition.*",
            )
        )
    elif not (instance_dir / composition_oracle).is_file():
        errors.append(
            CompletenessError(
                instance_id,
                f"composition_oracle references missing file: {composition_oracle}",
            )
        )

    if metadata.get("composition_expected") not in {"fail", "pass"}:
        errors.append(
            CompletenessError(
                instance_id,
                "metadata field composition_expected must be one of: fail, pass",
            )
        )


def check_reproduced_instance(
    instance: dict[str, Any],
    root: Path,
) -> list[CompletenessError]:
    instance_id = str(instance.get("id", "<unknown>"))
    errors: list[CompletenessError] = []

    path_value = instance.get("path")
    if not isinstance(path_value, str):
        return [CompletenessError(instance_id, "index entry path must be a string")]

    instance_dir = root / path_value
    if not instance_dir.is_dir():
        return [CompletenessError(instance_id, f"missing instance directory: {path_value}")]

    for relative_path in [
        "README.md",
        "metadata.json",
        "task_a.md",
        "task_b.md",
        "patch_a.patch",
        "patch_b.patch",
        "combined.patch",
        *REQUIRED_SCRIPTS,
        *REQUIRED_LOGS,
    ]:
        require_file(errors, instance_id, instance_dir, relative_path)

    for stem in ["test_patch_a", "test_patch_b", "test_composition"]:
        require_oracle(errors, instance_id, instance_dir, stem)

    metadata_path = instance_dir / "metadata.json"
    if metadata_path.is_file():
        metadata = load_json(metadata_path)
        if isinstance(metadata, dict):
            check_metadata_references(errors, instance_id, instance_dir, metadata)
        else:
            errors.append(CompletenessError(instance_id, "metadata.json must be an object"))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--index",
        type=Path,
        default=ROOT / "instances" / "index.json",
        help="Path to instances/index.json.",
    )
    args = parser.parse_args()

    instances = load_index(args.index)
    reproduced = [
        instance for instance in instances if instance.get("status") == "reproduced"
    ]

    errors: list[CompletenessError] = []
    for instance in reproduced:
        errors.extend(check_reproduced_instance(instance, ROOT))

    if errors:
        print("Instance completeness check failed:")
        for error in errors:
            print(f"- {error.instance_id}: {error.message}")
        return 1

    print(f"Instance completeness check passed for {len(reproduced)} reproduced instances.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
