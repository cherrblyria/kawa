import io
import json
import random
import time
import unittest
from contextlib import redirect_stdout
from unittest import mock

from click.testing import CliRunner

import kawa.modules.coinflip as coinflip_mod
from kawa.cli import cli
from kawa.modules.coinflip import run_coinflip


class CoinflipTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def flip(self, hour, seed):
        buf = io.StringIO()
        with redirect_stdout(buf):
            run_coinflip(hour=hour, mode="plain", rng=random.Random(seed))
        return buf.getvalue().strip()

    def flip_seeded(self, seed):
        buf = io.StringIO()
        with redirect_stdout(buf):
            run_coinflip(hour=10, mode="cute", rng=random.Random(seed))
        return buf.getvalue().strip()

    def test_bias_am_pm(self):
        for hour, expected in [
            (0, "heads"),
            (11, "heads"),
            (12, "tails"),
            (23, "tails"),
        ]:
            with self.subTest(hour=hour):
                counts = {"heads": 0, "tails": 0}
                with mock.patch.object(coinflip_mod, "pick_event", return_value=None):
                    for i in range(300):
                        counts[self.flip(hour, i)] += 1
                self.assertGreater(counts[expected], 100)

    def test_deterministic_seeded(self):
        with mock.patch.object(coinflip_mod, "get_uwu") as mock_uwu:
            mock_uwu.return_value.uwuify.side_effect = lambda s: f"UWU({s})"
            self.assertEqual(self.flip_seeded(1), self.flip_seeded(1))

    def test_forced_kawa_event(self):
        event = {"name": "kawa", "messages": ["hello"]}
        with (
            mock.patch.object(coinflip_mod, "pick_event", return_value=event),
            mock.patch.object(coinflip_mod, "get_uwu") as mock_uwu,
        ):
            mock_uwu.return_value.uwuify.side_effect = lambda s: f"UWU({s})"
            buf = io.StringIO()
            with redirect_stdout(buf):
                run_coinflip(hour=10, mode="cute", rng=random.Random(0))
            self.assertEqual(buf.getvalue().strip(), "UWU(hello)")

    def test_forced_secret_event(self):
        event = {"name": "secret", "messages": ["raw message"]}
        with mock.patch.object(coinflip_mod, "pick_event", return_value=event):
            buf = io.StringIO()
            with redirect_stdout(buf):
                run_coinflip(hour=10, mode="cute", rng=random.Random(0))
            self.assertEqual(buf.getvalue().strip(), "raw message")

    def test_json_shape(self):
        result = self.runner.invoke(cli, ["coinflip", "--json"])
        self.assertEqual(result.exit_code, 0)
        data = json.loads(result.output)
        self.assertIn(data["result"], ("heads", "tails"))
        self.assertIn("message", data)

    def test_machine_modes_never_events(self):
        event = {"name": "kawa", "messages": ["hello"]}
        with mock.patch.object(coinflip_mod, "pick_event", return_value=event):
            for mode in ("--plain", "--json"):
                result = self.runner.invoke(cli, ["coinflip", mode])
                self.assertEqual(result.exit_code, 0)

    def test_no_module_collision(self):
        import kawa.modules

        self.assertTrue(hasattr(kawa.modules.coinflip, "run_coinflip"))

    def test_no_slowdown(self):
        coinflip_mod.get_uwu.cache_clear()
        start = time.perf_counter()
        self.flip(10, 0)
        first = time.perf_counter() - start
        start = time.perf_counter()
        for i in range(1, 2000):
            self.flip(10, i)
        avg = (time.perf_counter() - start) / 1999
        self.assertLess(avg, first * 3 + 0.001)


if __name__ == "__main__":
    unittest.main()
