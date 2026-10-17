import os
import subprocess
import sys
import unittest


class EncodingTests(unittest.TestCase):
    def run_kawa(self, *args):
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "cp1252"
        return subprocess.run(
            [sys.executable, "-m", "kawa", *args],
            capture_output=True,
            text=True,
            env=env,
            cwd="/home/cherr/Projects/Coding/kawa/src",
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
