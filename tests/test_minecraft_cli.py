import json
import unittest

from click.testing import CliRunner

from kawa.cli import cli
from kawa.modules.minecraft import BORDER_MESSAGE, exp_for_level


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
        self.assertEqual(json.loads(result.output), {"level": 17, "experience": 394})

    def test_experience_to_level_json(self):
        result = self.runner.invoke(cli, ["mc", "xplv", "0", "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(json.loads(result.output), {"experience": 0, "level": 0})

    def test_negative_coordinates(self):
        result = self.runner.invoke(cli, ["mc", "ntow", "-5", "-3"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output.strip(),
            "(x: -5 y: -3) in Nether is (x: -40 y: -24) in Overworld  /ᐠ｡ꞈ｡ᐟ\\",
        )

    def test_negative_coordinates_json(self):
        result = self.runner.invoke(cli, ["mc", "ntow", "-5", "-3", "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(json.loads(result.output), {"x": -40, "z": -24})

    def test_negative_overworld_json(self):
        result = self.runner.invoke(cli, ["mc", "ownt", "-80", "-160", "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(json.loads(result.output), {"x": -10, "z": -20})

    def test_double_dash_still_works(self):
        result = self.runner.invoke(cli, ["mc", "ntow", "--", "-5", "-3"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("(x: -40 y: -24) in Overworld", result.output)

    def test_negative_level_rejected(self):
        result = self.runner.invoke(cli, ["mc", "lvxp", "-1"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("not in the range", result.output)

    def test_negative_xp_rejected(self):
        result = self.runner.invoke(cli, ["mc", "xplv", "-1"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("not in the range", result.output)

    def test_ntow_help(self):
        result = self.runner.invoke(cli, ["mc", "ntow", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Convert Nether coordinates", result.output)

    def test_ntow_short_help(self):
        result = self.runner.invoke(cli, ["mc", "ntow", "-h"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Convert Nether coordinates", result.output)

    def test_level_boundaries(self):
        cases = [(352, 16), (353, 16.025276020429825), (1507, 31.0)]
        for xp, expected in cases:
            with self.subTest(xp=xp):
                result = self.runner.invoke(cli, ["mc", "xplv", str(xp), "--json"])
                self.assertEqual(result.exit_code, 0)
                self.assertAlmostEqual(json.loads(result.output)["level"], expected)

    def test_easter_eggs(self):
        result = self.runner.invoke(cli, ["mc", "lvxp", "21863"])
        self.assertIn("maximum XP", result.output)
        result = self.runner.invoke(cli, ["mc", "lvxp", "21864"])
        self.assertIn("break the game", result.output)
        result = self.runner.invoke(cli, ["mc", "xplv", "2147483647"])
        self.assertIn("Have you ever reach", result.output)

    def test_roundtrip_every_level(self):
        for level in range(21864):
            xp = exp_for_level(level)
            result = self.runner.invoke(cli, ["mc", "xplv", str(xp), "--plain"])
            self.assertEqual(result.exit_code, 0, f"level {level}")
            self.assertEqual(int(result.output.strip()), level, f"level {level}")

    def test_xplv_exact_297845(self):
        result = self.runner.invoke(cli, ["mc", "xplv", "297845", "--plain"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.strip(), "275")

    def test_lvxp_huge_exact(self):
        result = self.runner.invoke(cli, ["mc", "lvxp", "1000000000", "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            json.loads(result.output),
            {"level": 1000000000, "experience": 4499999837500002220},
        )

    def test_lvxp_over_bound(self):
        result = self.runner.invoke(cli, ["mc", "lvxp", "10000000000"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("not in the range", result.output)

    def test_xplv_huge_rejected(self):
        result = self.runner.invoke(cli, ["mc", "xplv", "9" * 400])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("not in the range", result.output)

    def test_nan_rejected(self):
        result = self.runner.invoke(cli, ["mc", "ntow", "nan", "0"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("must be a finite number", result.output)

    def test_inf_rejected_json(self):
        result = self.runner.invoke(cli, ["mc", "ownt", "inf", "1", "--json"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("must be a finite number", result.output)

    def test_overflow_rejected(self):
        result = self.runner.invoke(cli, ["mc", "ntow", "1e308", "0"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("result out of range", result.output)

    def test_json_never_nan(self):
        cases = [
            ["mc", "ntow", "nan", "0", "--json"],
            ["mc", "ownt", "inf", "1", "--json"],
            ["mc", "ntow", "1e308", "0", "--json"],
        ]
        for args in cases:
            with self.subTest(args=args):
                result = self.runner.invoke(cli, args)
                self.assertEqual(result.exit_code, 2)
                self.assertNotIn("NaN", result.output)
                self.assertNotIn("Infinity", result.output)

    def test_readme_examples(self):
        result = self.runner.invoke(cli, ["mc", "ntow", "727", "90.875"])
        self.assertEqual(
            result.output.strip(),
            "(x: 727 y: 90.875) in Nether is (x: 5816 y: 727) in Overworld  /ᐠ｡ꞈ｡ᐟ\\",
        )
        result = self.runner.invoke(cli, ["mc", "lvxp", "21864"])
        self.assertIn(
            "Level 21,864 is 2,147,604,552 Experience /ᐠ｡‸｡ᐟ\\", result.output
        )
        result = self.runner.invoke(cli, ["mc", "xplv", "2147483647"])
        self.assertIn(
            "2,147,483,647 Experience is Level 21,863.39 /ᐠ｡‸｡ᐟ\\", result.output
        )

    def test_world_border_quip(self):
        result = self.runner.invoke(cli, ["mc", "ntow", "40000000", "0"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            any(msg in result.output for msg in BORDER_MESSAGE),
            f"expected one of {BORDER_MESSAGE!r}, got {result.output!r}",
        )

    def test_xp_boundaries(self):
        cases = [(16, 352), (17, 394), (30, 1395), (31, 1507), (32, 1628)]
        for level, expected in cases:
            with self.subTest(level=level):
                self.assertEqual(exp_for_level(level), expected)


if __name__ == "__main__":
    unittest.main()
