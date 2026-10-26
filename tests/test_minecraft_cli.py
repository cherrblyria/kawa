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


class MinecraftStorageCliTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def invoke(self, *args):
        return self.runner.invoke(cli, ["mc", *args])

    def test_exact_cute_examples(self):
        result = self.invoke("item", "128", "to-stack")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output.strip(), "that's 2 stack(s) of item(s) /ᐠ_ ꞈ _ᐟ\\ɴʏᴀ~"
        )
        result = self.invoke("stack", "9", "to-item", "-s", "16")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.strip(), "that's 144 item(s) /ᐠ_ ꞈ _ᐟ\\ɴʏᴀ~")

    def test_all_six_directions(self):
        cases = [
            (("item", "1728", "to-stack"), "that's 27 stack(s) of item(s)"),
            (("item", "1728", "to-shulker"), "that's 1 shulker box(es) of item(s)"),
            (("stack", "27", "to-item"), "that's 1,728 item(s)"),
            (("stack", "27", "to-shulker"), "that's 1 shulker box(es) of item(s)"),
            (("shulker", "1", "to-item"), "that's 1,728 item(s)"),
            (("shulker", "1", "to-stack"), "that's 27 stack(s) of item(s)"),
        ]
        for args, expected in cases:
            with self.subTest(args=args):
                result = self.invoke(*args)
                self.assertEqual(result.exit_code, 0, result.output)
                self.assertTrue(result.output.startswith(expected), result.output)

    def test_breakdowns(self):
        cases = [
            (("item", "100", "to-stack"), "that's 1 stack(s) and 36 item(s)"),
            (
                ("item", "1800", "to-shulker"),
                "that's 1 shulker box(es), 1 stack(s) and 8 item(s)",
            ),
            (("stack", "30", "to-shulker"), "that's 1 shulker box(es) and 3 stack(s)"),
            (
                ("stack", "60", "to-shulker", "-l"),
                "that's 1 large chest(s) and 6 stack(s)",
            ),
            (
                ("item", "100", "to-stack", "-s", "16"),
                "that's 6 stack(s) and 4 item(s)",
            ),
        ]
        for args, expected in cases:
            with self.subTest(args=args):
                result = self.invoke(*args)
                self.assertEqual(result.exit_code, 0, result.output)
                self.assertTrue(result.output.startswith(expected), result.output)

    def test_plain_and_json(self):
        result = self.invoke("item", "100", "to-stack", "--plain")
        self.assertEqual(result.output.strip(), "1.5625")
        result = self.invoke("item", "100", "to-stack", "--json")
        data = json.loads(result.output)
        self.assertEqual(data["result"], 1.5625)
        self.assertEqual(data["breakdown"], {"stack": 1, "item": 36})
        result = self.invoke("item", "128", "to-stack", "--json")
        self.assertNotIn("breakdown", json.loads(result.output))

    def test_large_chest_and_aliases(self):
        result = self.invoke("shulker", "1", "to-item", "-l")
        self.assertIn("3,456 item(s)", result.output)
        result = self.invoke("sb", "1", "to-item", "--plain")
        self.assertEqual(result.output.strip(), "1728")
        result = self.invoke("item", "128", "to-sb", "--plain")
        self.assertEqual(result.output.strip(), "0.07407407407407407")

    def test_large_chest_json_breakdown_uses_container_name(self):
        result = self.invoke("item", "3457", "to-shulker", "-l", "--json")
        self.assertEqual(result.exit_code, 0, result.output)
        data = json.loads(result.output)
        self.assertEqual(data["container"], "large_chest")
        self.assertEqual(data["breakdown"], {"large_chest": 1, "item": 1})

    def test_stack_sizes_and_zero_identity(self):
        for size in (1, 16, 64, 1000):
            with self.subTest(size=size):
                result = self.invoke(
                    "stack", "9", "to-item", "-s", str(size), "--plain"
                )
                self.assertEqual(result.exit_code, 0)
                self.assertEqual(result.output.strip(), str(9 * size))
        self.assertEqual(
            self.invoke("item", "0", "to-stack", "--plain").output.strip(), "0"
        )
        self.assertEqual(
            self.invoke("item", "9", "to-item", "--plain").output.strip(), "9"
        )

    def test_maximum_amount_and_large_stack_size(self):
        result = self.invoke("item", "1000000000000000000", "to-item", "--plain")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.strip(), "1000000000000000000")
        large_stack_size = "9" * 400
        result = self.invoke("stack", "1", "to-item", "-s", large_stack_size, "--plain")
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output.strip(), large_stack_size)

    def test_invalid_arguments(self):
        for args in (
            ("item", "-5", "to-stack"),
            ("item", "1", "to-stack", "-s", "0"),
            ("item", "1", "bad-target"),
            ("item", "1", "to-stack", "--json", "--plain"),
        ):
            with self.subTest(args=args):
                result = self.invoke(*args)
                self.assertEqual(result.exit_code, 2)

    def test_help(self):
        for command in ("item", "stack", "shulker", "sb"):
            with self.subTest(command=command):
                result = self.invoke(command, "--help")
                self.assertEqual(result.exit_code, 0)
                self.assertIn("Convert", result.output)


if __name__ == "__main__":
    unittest.main()
