import json
import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner

from kawa.cli import cli


class JsonCliTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def write(self, tmp, name, content, encoding="utf-8"):
        target = Path(tmp) / name
        target.write_text(content, encoding=encoding)
        return str(target)

    def test_raw_string(self):
        result = self.runner.invoke(cli, ["json", "pretty", '{"b": 1, "a": 2}'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(json.loads(result.output), {"b": 1, "a": 2})

    def test_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.write(tmp, "data.json", '{"b": 1, "a": 2}')
            result = self.runner.invoke(cli, ["json", "pretty", target])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(json.loads(result.output), {"b": 1, "a": 2})

    def test_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.write(tmp, "bom.json", '{"a": 1}', encoding="utf-8-sig")
            result = self.runner.invoke(cli, ["json", "pretty", target])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(json.loads(result.output), {"a": 1})

    def test_utf16_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.write(tmp, "utf16.json", '{"a": 1}', encoding="utf-16")
            result = self.runner.invoke(cli, ["json", "pretty", target])
            self.assertEqual(result.exit_code, 1)
            self.assertIn("Error:", result.output)
            self.assertNotIn("Traceback", result.output)

    def test_bigint_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.write(tmp, "big.json", '{"n": ' + "9" * 4400 + "}")
            result = self.runner.invoke(cli, ["json", "pretty", target])
            self.assertEqual(result.exit_code, 1)
            self.assertIn("Error:", result.output)

    def test_deep_nesting_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.write(tmp, "deep.json", "[" * 200000)
            result = self.runner.invoke(cli, ["json", "pretty", target])
            self.assertEqual(result.exit_code, 1)
            self.assertIn("Error:", result.output)

    def test_surrogate_escaped(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.write(tmp, "sur.json", '{"s": "\\ud800"}')
            result = self.runner.invoke(cli, ["json", "pretty", target])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("\\ud800", result.output)

    def test_nan_rejected(self):
        result = self.runner.invoke(cli, ["json", "pretty", '{"n": NaN}'])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("NaN is not allowed", result.output)

    def test_inf_float_rejected(self):
        result = self.runner.invoke(cli, ["json", "pretty", "1e999"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Error:", result.output)

    def test_indent_bounds(self):
        result = self.runner.invoke(
            cli, ["json", "pretty", "--indent", "100000000", '{"a": 1}']
        )
        self.assertEqual(result.exit_code, 2)
        result = self.runner.invoke(
            cli, ["json", "pretty", "--indent", "-1", '{"a": 1}']
        )
        self.assertEqual(result.exit_code, 2)

    def test_sort_keys(self):
        result = self.runner.invoke(
            cli, ["json", "pretty", '{"b": 1, "a": 2}', "--sort-keys"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertLess(result.output.index('"a"'), result.output.index('"b"'))

    def test_dup_keys_warn(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.write(tmp, "dup.json", '{"a": 1, "a": 2}')
            result = self.runner.invoke(cli, ["json", "pretty", target])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("duplicate key", result.output)
            self.assertEqual(json.loads(result.output.split("\n", 1)[1]), {"a": 2})

    def test_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            sub = Path(tmp) / "adir"
            sub.mkdir()
            result = self.runner.invoke(cli, ["json", "pretty", str(sub)])
            self.assertEqual(result.exit_code, 1)
            self.assertIn("is a directory", result.output)

    def test_missing_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = str(Path(tmp) / "missing.json")
            result = self.runner.invoke(cli, ["json", "pretty", target])
            self.assertEqual(result.exit_code, 1)
            self.assertIn("File not found", result.output)

    def test_missing_txt(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = str(Path(tmp) / "test.txt")
            result = self.runner.invoke(cli, ["json", "pretty", target])
            self.assertEqual(result.exit_code, 1)
            self.assertIn("File not found", result.output)

    def test_stdin(self):
        result = self.runner.invoke(cli, ["json", "pretty", "-"], input='{"a": 1}')
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(json.loads(result.output), {"a": 1})

    def test_unicode_preserved(self):
        result = self.runner.invoke(cli, ["json", "pretty", '{"t": "สวัสดี"}'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("สวัสดี", result.output)


if __name__ == "__main__":
    unittest.main()
