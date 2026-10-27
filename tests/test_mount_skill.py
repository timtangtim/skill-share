"""Installer regression tests; all writes use a temporary HOME."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "mount-skill.sh"
TARGETS = (".agents/skills", ".config/opencode/skills", ".gemini/config/skills")

class MountTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="skill-share-test-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.home = self.root / "test home"
        self.home.mkdir()
        self.skill = self.root / "source with spaces" / "demo-skill"
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            "---\nname: demo-skill\ndescription: Test skill\n---\nInstructions\n")

    def mount(self, *args, env=None):
        return subprocess.run(["bash", str(SCRIPT), *map(str, args)],
            env={**os.environ, "HOME": str(self.home), **(env or {})},
            cwd=self.root, capture_output=True, text=True)

    def test_links_relative_paths_spaces_and_repeat(self):
        for _ in range(2):
            result = self.mount(self.skill.relative_to(self.root))
            self.assertEqual(result.returncode, 0, result.stderr)
            for target in TARGETS:
                link = self.home / target / self.skill.name
                self.assertTrue(link.is_symlink())
                self.assertEqual(link.resolve(), self.skill.resolve())
        (self.skill / "reference.txt").write_text("updated")
        for target in TARGETS:
            self.assertEqual((self.home / target / self.skill.name / "reference.txt").read_text(), "updated")

    def test_invalid_arguments(self):
        for args in [(), (self.skill, "extra"), ("missing",), (self.skill / "SKILL.md",)]:
            with self.subTest(args=args):
                self.assertNotEqual(self.mount(*args).returncode, 0)
        self.assertFalse((self.home / ".agents").exists())

    def test_missing_empty_manifest(self):
        manifest = self.skill / "SKILL.md"
        manifest.unlink()
        self.assertNotEqual(self.mount(self.skill).returncode, 0)
        manifest.touch()
        self.assertNotEqual(self.mount(self.skill).returncode, 0)
        self.assertFalse((self.home / ".agents").exists())

    def test_invalid_names(self):
        for name in ["Upper", "bad--name", "-bad", "bad-", "a" * 65]:
            with self.subTest(name=name):
                invalid = self.root / name
                invalid.mkdir()
                (invalid / "SKILL.md").write_text("test")
                self.assertNotEqual(self.mount(invalid).returncode, 0)
        self.assertFalse((self.home / ".agents").exists())

    def test_conflicts_preserved_and_preflighted(self):
        conflict = self.home / TARGETS[-1] / self.skill.name
        conflict.parent.mkdir(parents=True)
        other = self.root / "other"
        other.mkdir()
        for kind in ["file", "directory", "link", "broken-link"]:
            with self.subTest(kind=kind):
                if kind == "file":
                    conflict.write_text("keep me")
                elif kind == "directory":
                    conflict.mkdir()
                    (conflict / "keep.txt").write_text("keep me")
                else:
                    conflict.symlink_to(other if kind == "link" else self.root / "missing")
                self.assertNotEqual(self.mount(self.skill).returncode, 0)
                self.assertFalse((self.home / ".agents").exists())
                if kind == "file":
                    self.assertEqual(conflict.read_text(), "keep me")
                elif kind == "directory":
                    self.assertEqual((conflict / "keep.txt").read_text(), "keep me")
                    (conflict / "keep.txt").unlink()
                    conflict.rmdir()
                    continue
                else:
                    self.assertEqual(os.readlink(conflict), str(other if kind == "link" else self.root / "missing"))
                conflict.unlink()

    def test_blocked_parent(self):
        (self.home / ".gemini").write_text("keep me")
        self.assertNotEqual(self.mount(self.skill).returncode, 0)
        self.assertFalse((self.home / ".agents").exists())

    def test_invalid_home(self):
        for home in ["", "relative"]:
            self.assertNotEqual(self.mount(self.skill, env={"HOME": home}).returncode, 0)

    def test_link_failure_never_reports_success(self):
        tools = self.root / "bin"
        tools.mkdir()
        fake_ln = tools / "ln"
        fake_ln.write_text("#!/bin/sh\nexit 1\n")
        fake_ln.chmod(0o755)
        result = self.mount(self.skill, env={"PATH": f"{tools}:{os.environ['PATH']}"})
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Done!", result.stdout)

    def batch_repo(self):
        repo = self.root / "repo with spaces"
        repo.mkdir()
        shutil.copy2(SCRIPT, repo / "mount-skill.sh")
        (repo / "skill").mkdir()
        return repo

    def mount_all(self, repo):
        return subprocess.run(["bash", str(repo / "mount-skill.sh"), "--all"],
            env={**os.environ, "HOME": str(self.home)}, cwd=self.root,
            capture_output=True, text=True)

    def batch_skill(self, repo, name):
        skill = repo / "skill" / name
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Test skill\n---\nInstructions\n")
        return skill

    def test_all_mounts_multiple_skills_from_script_directory(self):
        repo = self.batch_repo()
        skills = [self.batch_skill(repo, name) for name in ["alpha", "beta"]]
        (repo / "skill" / ".gitkeep").touch()
        (repo / "skill" / "notes.txt").write_text("ignore")
        for _ in range(2):
            result = self.mount_all(repo)
            self.assertEqual(result.returncode, 0, result.stderr)
            for skill in skills:
                for target in TARGETS:
                    link = self.home / target / skill.name
                    self.assertTrue(link.is_symlink())
                    self.assertEqual(link.resolve(), skill.resolve())

    def test_all_empty_directory_does_nothing(self):
        repo = self.batch_repo()
        (repo / "skill" / ".gitkeep").touch()
        result = self.mount_all(repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Nothing to mount", result.stdout)
        self.assertFalse((self.home / ".agents").exists())

    def test_all_invalid_later_skill_prevents_entire_batch(self):
        repo = self.batch_repo()
        self.batch_skill(repo, "alpha")
        (repo / "skill" / "beta").mkdir()
        self.assertNotEqual(self.mount_all(repo).returncode, 0)
        self.assertFalse((self.home / ".agents").exists())

    def test_all_later_conflict_preserves_entire_batch(self):
        repo = self.batch_repo()
        self.batch_skill(repo, "alpha")
        self.batch_skill(repo, "beta")
        conflict = self.home / TARGETS[-1] / "beta"
        conflict.parent.mkdir(parents=True)
        conflict.write_text("keep me")
        self.assertNotEqual(self.mount_all(repo).returncode, 0)
        self.assertEqual(conflict.read_text(), "keep me")
        self.assertFalse((self.home / ".agents").exists())

    def test_all_duplicate_resolved_names_prevent_mount(self):
        repo = self.batch_repo()
        skill = self.batch_skill(repo, "alpha")
        (repo / "skill" / "alias").symlink_to(skill)
        self.assertNotEqual(self.mount_all(repo).returncode, 0)
        self.assertFalse((self.home / ".agents").exists())

    def test_all_missing_skill_directory(self):
        repo = self.batch_repo()
        (repo / "skill").rmdir()
        self.assertNotEqual(self.mount_all(repo).returncode, 0)
        self.assertFalse((self.home / ".agents").exists())

if __name__ == "__main__":
    unittest.main()
