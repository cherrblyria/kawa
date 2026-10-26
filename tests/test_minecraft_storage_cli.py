import json
import unittest

from click.testing import CliRunner

from kawa.cli import cli


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
        result = self.invoke(
            "stack", "1", "to-item", "-s", large_stack_size, "--plain"
        )
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
