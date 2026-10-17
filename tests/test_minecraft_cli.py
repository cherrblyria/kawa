import json
import unittest

from click.testing import CliRunner

from kawa.cli import cli


class MinecraftCliTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_nether_to_overworld_json(self):
        result = self.runner.invoke(cli, ["mc", "ntow", "10", "20", "--json"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(json.loads(result.output), {"x": 80, "z": 160})

    def test_overworld_to_nether_json(self):
        result = self.runner.invoke(cli, ["mc", "ownt", "80", "160", "--json"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(json.loads(result.output), {"x": 10, "z": 20})

    def test_level_to_experience_json(self):
        result = self.runner.invoke(cli, ["mc", "lvxp", "17", "--json"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            json.loads(result.output), {"level": 17, "experience": 394}
        )

    def test_experience_to_level_json(self):
        result = self.runner.invoke(cli, ["mc", "xplv", "0", "--json"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            json.loads(result.output), {"experience": 0, "level": 0}
        )


if __name__ == "__main__":
    unittest.main()
