from pathlib import Path
import os
import subprocess
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"


class EncodingTests(unittest.TestCase):
    def run_kawa(self, *args):
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "cp1252"
        existing_pythonpath = env.get("PYTHONPATH")
        env["PYTHONPATH"] = (
            str(SRC_DIR)
            if not existing_pythonpath
            else os.pathsep.join((str(SRC_DIR), existing_pythonpath))
        )
        return subprocess.run(
            [sys.executable, "-m", "kawa", *args],
            capture_output=True,
            text=True,
            env=env,
            cwd=REPO_ROOT,
            check=False,
        )

    def test_cp1252_ntow(self):
        result = self.run_kawa("mc", "ntow", "1", "2")
        self.assertEqual(result.returncode, 0)

    def test_cp1252_version(self):
        result = self.run_kawa("-v")
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
