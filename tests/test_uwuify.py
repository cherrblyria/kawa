import json
import unittest
from unittest import mock

from click.testing import CliRunner

import kawa.modules.uwuify as uwuify_mod
from kawa.cli import cli


class UwuifyTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_empty_arg(self):
        with mock.patch.object(uwuify_mod, "get_uwu") as mock_uwu:
            mock_uwu.return_value.uwuify.side_effect = lambda s: f"UWU({s})"
            result = self.runner.invoke(cli, ["uwuify", ""])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.output.strip(), "UWU()")

    def test_multiple_args(self):
        with mock.patch.object(uwuify_mod, "get_uwu") as mock_uwu:
            mock_uwu.return_value.uwuify.side_effect = lambda s: f"UWU({s})"
            result = self.runner.invoke(cli, ["uwuify", "hello", "world"])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.output.strip(), "UWU(hello) UWU(world)")

    def test_json_shape(self):
        with mock.patch.object(uwuify_mod, "get_uwu") as mock_uwu:
            mock_uwu.return_value.uwuify.side_effect = lambda s: f"UWU({s})"
            result = self.runner.invoke(cli, ["uwuify", "--json", "hello", "world"])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(
                json.loads(result.output), {"result": "UWU(hello) UWU(world)"}
            )

    def test_newline_preserved(self):
        with mock.patch.object(uwuify_mod, "get_uwu") as mock_uwu:
            mock_uwu.return_value.uwuify.side_effect = lambda s: s
            result = self.runner.invoke(cli, ["uwuify", "a\nb"])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("a\nb", result.output)

    def test_passthrough_stubbed(self):
        with mock.patch.object(uwuify_mod, "get_uwu") as mock_uwu:
            mock_uwu.return_value.uwuify.side_effect = lambda s: s
            result = self.runner.invoke(
                cli, ["uwuify", "https://example.com", "@user", "สวัสดี"]
            )
            self.assertEqual(result.exit_code, 0)
            self.assertIn("https://example.com", result.output)
            self.assertIn("@user", result.output)
            self.assertIn("สวัสดี", result.output)


if __name__ == "__main__":
    unittest.main()
