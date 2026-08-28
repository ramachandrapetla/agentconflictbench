from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "run_instance.py"
SPEC = importlib.util.spec_from_file_location("run_instance", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
run_instance = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = run_instance
SPEC.loader.exec_module(run_instance)


class RunInstanceGitCleanupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        self.git("init", "-b", "main")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test User")

        tracked = self.repo / "tracked.txt"
        tracked.write_text("base\n")
        self.git("add", "tracked.txt")
        self.git("commit", "-m", "base")
        self.base_commit = self.git_output("rev-parse", "HEAD")

        tracked.write_text("main\n")
        self.git("commit", "-am", "main change")
        self.main_commit = self.git_output("rev-parse", "HEAD")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def git(self, *args: str) -> None:
        subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True)

    def git_output(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.repo, text=True).strip()

    def test_restore_checkout_returns_to_original_branch_and_commit(self) -> None:
        original = run_instance.get_checkout_state(self.repo)
        self.assertEqual(original.branch, "main")
        self.assertEqual(original.commit, self.main_commit)

        run_instance.checkout_base(self.repo, self.base_commit)
        (self.repo / "tracked.txt").write_text("patched\n")
        (self.repo / "created-by-patch.txt").write_text("temporary\n")

        run_instance.restore_checkout(self.repo, original)

        self.assertEqual(self.git_output("branch", "--show-current"), "main")
        self.assertEqual(self.git_output("rev-parse", "HEAD"), self.main_commit)
        self.assertEqual(self.git_output("status", "--short"), "")
        self.assertFalse((self.repo / "created-by-patch.txt").exists())
        self.assertEqual((self.repo / "tracked.txt").read_text(), "main\n")

    def test_restore_checkout_preserves_original_detached_head(self) -> None:
        self.git("checkout", "--detach", self.base_commit)
        original = run_instance.get_checkout_state(self.repo)
        self.assertIsNone(original.branch)
        self.assertEqual(original.commit, self.base_commit)

        self.git("switch", "main")
        (self.repo / "tracked.txt").write_text("patched\n")

        run_instance.restore_checkout(self.repo, original)

        self.assertEqual(self.git_output("branch", "--show-current"), "")
        self.assertEqual(self.git_output("rev-parse", "HEAD"), self.base_commit)
        self.assertEqual(self.git_output("status", "--short"), "")

    def test_reset_repo_removes_phase_changes_and_untracked_files(self) -> None:
        (self.repo / "tracked.txt").write_text("patched\n")
        (self.repo / "created-by-patch.txt").write_text("temporary\n")

        run_instance.reset_repo(self.repo)

        self.assertEqual((self.repo / "tracked.txt").read_text(), "main\n")
        self.assertFalse((self.repo / "created-by-patch.txt").exists())
        self.assertEqual(self.git_output("status", "--short"), "")


if __name__ == "__main__":
    unittest.main()
