import json
import unittest
import uuid

from click.testing import CliRunner

from kawa.cli import cli
from kawa.modules.uuid_tools import KAOMOJI


class UuidCliTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def generate(self, *args):
        result = self.runner.invoke(cli, ["uuid", *args])
        self.assertEqual(result.exit_code, 0, result.output)
        return result.output.strip()

    def test_default_is_v4(self):
        parsed = uuid.UUID(self.generate().removesuffix(KAOMOJI))
        self.assertEqual(parsed.version, 4)
        self.assertEqual(parsed.variant, uuid.RFC_4122)

    def test_v7_option(self):
        parsed = uuid.UUID(self.generate("--v7").removesuffix(KAOMOJI))
        self.assertEqual(parsed.version, 7)
        self.assertEqual(parsed.variant, uuid.RFC_4122)

    def test_plain_is_bare_uuid(self):
        output = self.generate("--plain")
        self.assertEqual(str(uuid.UUID(output)), output)

    def test_cute_has_kaomoji(self):
        output = self.generate()
        self.assertTrue(output.endswith(KAOMOJI))
        parsed = uuid.UUID(output.removesuffix(KAOMOJI))
        self.assertEqual(parsed.version, 4)

    def test_json_shape(self):
        data = json.loads(self.generate("--json"))
        self.assertEqual(data["version"], 4)
        self.assertEqual(uuid.UUID(data["uuid"]).version, 4)

    def test_json_v7_shape(self):
        data = json.loads(self.generate("--v7", "--json"))
        self.assertEqual(data["version"], 7)
        self.assertEqual(uuid.UUID(data["uuid"]).version, 7)

    def test_generates_different_values(self):
        self.assertNotEqual(self.generate("--plain"), self.generate("--plain"))

    def test_mode_flags_mutually_exclusive(self):
        result = self.runner.invoke(cli, ["uuid", "--json", "--plain"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("mutually exclusive", result.output)

    def test_help(self):
        result = self.runner.invoke(cli, ["uuid", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Generate a random UUID", result.output)


if __name__ == "__main__":
    unittest.main()
