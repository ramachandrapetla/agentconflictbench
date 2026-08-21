#!/usr/bin/env python3
"""Validate AgentConflictBench metadata and file references.

This script deliberately uses only the Python standard library so metadata
checks can run in fresh clones without requiring a package install.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
CONVENTIONAL_INSTANCE_FILES = [
    "task_a.md",
    "task_b.md",
    "combined.patch",
]


@dataclass(frozen=True)
class ValidationError:
    path: Path
    message: str


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        raise SystemExit(f"Missing JSON file: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from None


def schema_required_fields(schema: dict[str, Any]) -> set[str]:
    required = schema.get("required", [])
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        raise SystemExit("Schema field 'required' must be a list of strings.")

    return set(required)


def schema_enum_values(schema: dict[str, Any]) -> dict[str, set[str]]:
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        raise SystemExit("Schema field 'properties' must be an object.")

    enum_values: dict[str, set[str]] = {}
    for field, spec in properties.items():
        if not isinstance(spec, dict) or "enum" not in spec:
            continue

        values = spec["enum"]
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise SystemExit(f"Schema enum for {field!r} must be a list of strings.")

        enum_values[field] = set(values)

    return enum_values


def schema_property_names(schema: dict[str, Any]) -> set[str]:
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        raise SystemExit("Schema field 'properties' must be an object.")

    return set(properties)


def validate_metadata_file(
    metadata_path: Path,
    required: set[str],
    allowed_properties: set[str],
    enums: dict[str, set[str]],
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    metadata = load_json(metadata_path)

    if not isinstance(metadata, dict):
        return [ValidationError(metadata_path, "metadata must be a JSON object")]

    missing = sorted(required - set(metadata))
    for field in missing:
        errors.append(ValidationError(metadata_path, f"missing required field: {field}"))

    extra = sorted(set(metadata) - allowed_properties)
    for field in extra:
        errors.append(ValidationError(metadata_path, f"unknown field: {field}"))

    for field, allowed_values in enums.items():
        if field in metadata and metadata[field] not in allowed_values:
            allowed = ", ".join(sorted(allowed_values))
            errors.append(
                ValidationError(
                    metadata_path,
                    f"{field}={metadata[field]!r} is not one of: {allowed}",
                )
            )

    for field in ["id", "repo", "base_commit", "language"]:
        if field in metadata and not isinstance(metadata[field], str):
            errors.append(ValidationError(metadata_path, f"{field} must be a string"))

    if isinstance(metadata.get("base_commit"), str) and not COMMIT_RE.match(
        metadata["base_commit"]
    ):
        errors.append(
            ValidationError(metadata_path, "base_commit must be a 40-character SHA")
        )

    if metadata.get("human_modified") is not None and not isinstance(
        metadata["human_modified"], bool
    ):
        errors.append(ValidationError(metadata_path, "human_modified must be boolean"))

    instance_dir = metadata_path.parent
    for relative_path in CONVENTIONAL_INSTANCE_FILES:
        if not (instance_dir / relative_path).exists():
            errors.append(
                ValidationError(
                    metadata_path,
                    f"missing conventional instance file: {relative_path}",
                )
            )

    for field in [
        "patch_a",
        "patch_b",
        "validation_a",
        "validation_b",
        "composition_oracle",
    ]:
        value = metadata.get(field)
        if isinstance(value, str) and not (instance_dir / value).exists():
            errors.append(
                ValidationError(metadata_path, f"{field} references missing file: {value}")
            )

    return errors


def validate_index(index_path: Path, metadata_by_id: dict[str, dict[str, Any]]) -> list[ValidationError]:
    errors: list[ValidationError] = []
    index = load_json(index_path)

    if not isinstance(index, dict):
        return [ValidationError(index_path, "index must be a JSON object")]

    if index.get("schema_version") != 1:
        errors.append(ValidationError(index_path, "schema_version must be 1"))

    instances = index.get("instances")
    if not isinstance(instances, list):
        return errors + [ValidationError(index_path, "instances must be a list")]

    seen_ids: set[str] = set()
    allowed_statuses = {"candidate", "reproduced", "deprecated"}

    for offset, entry in enumerate(instances):
        location = f"instances[{offset}]"
        if not isinstance(entry, dict):
            errors.append(ValidationError(index_path, f"{location} must be an object"))
            continue

        entry_id = entry.get("id")
        entry_path = entry.get("path")

        if not isinstance(entry_id, str):
            errors.append(ValidationError(index_path, f"{location}.id must be a string"))
            continue

        if entry_id in seen_ids:
            errors.append(ValidationError(index_path, f"duplicate instance id: {entry_id}"))
        seen_ids.add(entry_id)

        metadata = metadata_by_id.get(entry_id)
        if metadata is None:
            errors.append(
                ValidationError(index_path, f"{entry_id} missing matching metadata.json")
            )
            continue

        for field in ["repo", "base_commit", "language", "conflict_type", "source"]:
            if entry.get(field) != metadata.get(field):
                errors.append(
                    ValidationError(
                        index_path,
                        f"{entry_id}.{field} does not match metadata.json",
                    )
                )

        if entry_path != f"instances/{entry_id}":
            errors.append(
                ValidationError(
                    index_path,
                    f"{entry_id}.path must be instances/{entry_id}",
                )
            )

        status = entry.get("status")
        if status not in allowed_statuses:
            allowed = ", ".join(sorted(allowed_statuses))
            errors.append(
                ValidationError(index_path, f"{entry_id}.status must be one of: {allowed}")
            )

    missing_from_index = sorted(set(metadata_by_id) - seen_ids)
    for instance_id in missing_from_index:
        errors.append(ValidationError(index_path, f"{instance_id} missing from index"))

    return errors


def collect_metadata(instance_root: Path) -> dict[str, dict[str, Any]]:
    metadata_by_id: dict[str, dict[str, Any]] = {}

    for metadata_path in sorted(instance_root.glob("*/metadata.json")):
        metadata = load_json(metadata_path)
        if not isinstance(metadata, dict) or not isinstance(metadata.get("id"), str):
            continue

        metadata_by_id[metadata["id"]] = metadata

    return metadata_by_id


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--schema",
        type=Path,
        default=ROOT / "schema" / "metadata.schema.json",
        help="Path to the metadata JSON schema.",
    )
    parser.add_argument(
        "--instances",
        type=Path,
        default=ROOT / "instances",
        help="Path to the instance directory.",
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=ROOT / "instances" / "index.json",
        help="Path to the dataset index.",
    )
    args = parser.parse_args()

    schema = load_json(args.schema)
    if not isinstance(schema, dict):
        raise SystemExit(f"Schema must be a JSON object: {args.schema}")

    required = schema_required_fields(schema)
    allowed_properties = schema_property_names(schema)
    enums = schema_enum_values(schema)

    metadata_paths = sorted(args.instances.glob("*/metadata.json"))
    errors: list[ValidationError] = []
    metadata_by_id: dict[str, dict[str, Any]] = {}

    for metadata_path in metadata_paths:
        errors.extend(
            validate_metadata_file(metadata_path, required, allowed_properties, enums)
        )
        metadata = load_json(metadata_path)
        if isinstance(metadata, dict) and isinstance(metadata.get("id"), str):
            metadata_by_id[metadata["id"]] = metadata

            expected_path = args.instances / metadata["id"] / "metadata.json"
            if metadata_path != expected_path:
                errors.append(
                    ValidationError(
                        metadata_path,
                        f"metadata path should be {expected_path}",
                    )
                )

    errors.extend(validate_index(args.index, metadata_by_id))

    if errors:
        print("Metadata validation failed:\n")
        for error in errors:
            print(f"- {error.path}: {error.message}")
        return 1

    print(f"Metadata validation passed for {len(metadata_paths)} instances.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
