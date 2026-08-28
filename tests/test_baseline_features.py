from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "baseline_features.py"
SPEC = importlib.util.spec_from_file_location("baseline_features", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
baseline_features = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = baseline_features
SPEC.loader.exec_module(baseline_features)


class BaselineFeaturesTests(unittest.TestCase):
    def test_empty_index_writes_header_only_csv(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            index = temp / "index.json"
            output = temp / "features.csv"
            index.write_text(json.dumps({"instances": []}))

            completed = subprocess.run(
                [
                    sys.executable,
                    str(MODULE_PATH),
                    "--index",
                    str(index),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            with output.open(newline="") as csv_file:
                reader = csv.reader(csv_file)
                rows = list(reader)

            self.assertEqual(rows, [baseline_features.BASELINE_FIELDS])
            self.assertIn("Wrote 0 rows", completed.stdout)


if __name__ == "__main__":
    unittest.main()
