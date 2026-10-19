# Active Context

## Current Work Focus

Edge-case audit **merged** (PR #4, `fix/edge-cases` into `main`, HEAD `0a10611` == `origin/main`). Follow-ups: README trim (`b9fe2ac`, tagged `v0.3.2`), code bumped to **0.3.1** (`2dd4856`/`d758923`/`9083713`), test PR #3, ruff-enforcement PR #2, negative-input PR #1. Suite is **58 tests on main** (minecraft 26, json 17, coinflip 8, uwuify 5, encoding 2) via `python -m unittest discover -s tests -v` in CI (ubuntu + windows jobs); **working tree runs 58 green** (format drift resolved, see below).

**Uncommitted working tree (all differ from `0a10611`):** `cli.py` UTF-8 startup uses `getattr`+`callable` (fixes Pylance `reconfigure` unknown-attribute on `TextIO`); `minecraft.py` cute-output rework (kaomoji style, 4-message `BORDER_MESSAGE` list, `rng` injection, `xp_for_level` renamed to `exp_for_level`); `coinflip.py` blank-line reformat + `rng` None-guards; `tests/test_minecraft_cli.py` asserts the new kaomoji format (4 drifted tests fixed 2026-10-20: `test_negative_coordinates`, `test_double_dash_still_works`, `test_readme_examples` updated; `test_world_border_quip` now asserts `any(BORDER_MESSAGE)` since only 1 of 4 random messages matched the old `world border` substring; dead `test_xp_boundaries` revived from under `if __name__`, suite 57 to 58). README examples updated to new style 2026-10-20. Old `ownt` tuple bug is fixed - both converters use `rng.choice(BORDER_MESSAGE)`.

Conventions: `run_*` names (`run_coinflip`, `run_uwuify`) with explicit `__all__`; lazy cached `Uwuipy` via `functools.cache get_uwu()` per module; `rng` injection in coinflip + minecraft converters; `click.IntRange` bounds (level ≤ 1e9, xp ≤ 1e18, indent 0..16); `--json`+`--plain` → `UsageError`; UTF-8 streams forced at startup; `FiniteFloat` rejects NaN/inf; `MC_CONTEXT_SETTINGS` on `mc` leaves for negative numbers.

Coinflip shape: `EASTER_EGG_EVENTS`/`pick_event` (kawa 1/100, secret 1/100K), `COINS_MESSAGES` (8 fragments), `KAWA_MESSAGES` (5), `SECRET_PLACEHOLDER_MESSAGES` (4, "nutty the dev" voice). No dependency on `modules/uwuify.py` (`3056e31`). Only `kawa` is uwuified; `secret` prints raw and awaits the user's lore design.

## Recent Changes (newest first)

- `0a10611` merge main (HEAD == origin/main)
- `9083713` + `2dd4856` + `d758923` bump code to 0.3.1
- `b9fe2ac` docs(readme): human slop (tag **v0.3.2**) — warning banner, trimmed sections, Output-modes restored
- `c74297a` Merge PR #4 `fix/edge-cases` (`6611d10` mc → `9ef1b2d` json → `adc030f` UTF-8 → `e01def6` internals → `0a8543a` docs/sync)
- `f9f39ad` Merge PR #3 test suite; `3eafe87` Merge PR #2 blocking ruff; `15d3f89` Merge PR #1 non-negative XP/level
- `62a34a2` docs(readme): sort (tag **v0.3.1**)
- Older: `34d4f42` memory-bank sync; `3056e31` coinflip→uwuipy direct; `151b8cc` coinflip repair; `f69ecbe` uwuify-coinflip WIP; `2e04c07` EASTER_EGG_EVENTS refactor; `acc29c9` README trim

## Next Steps / Likely Future Work

- **Resolve version/tag mismatch**: code is 0.3.1 but latest tag is v0.3.2, and both v0.3.1/v0.3.2 predate the code bump. Pick one version, bump both files together, retag if needed.
- ~~Fix uncommitted `ownt` bug~~ **done in tree** (both converters use `rng.choice`); still uncommitted.
- Decide the mc cute rework (coords AND xp/level + 4 random borders + exp_for_level rename): commit or revert. Tests now green (58/58); README updated to new format. Old line below superseded: (new `/ᐠ｡ꞈ｡ᐟ\` style + random borders): commit (fixing `ownt`) or revert. If kept, update README + 26 minecraft tests.
- Design the **lore/interactive coinflip event** with the user; replace `SECRET_PLACEHOLDER_MESSAGES` then.
- Add more "useless cute" tools; possible `CHANGELOG.md`, PyPI publishing, man page.


## Active Decisions & Considerations

- **Python 3.14 is a hard floor** (`requires-python = ">=3.14"`, `.python-version` = `3.14`, flake uses `pkgs.python314`). Code relies on `int.is_integer()` (3.12+) via `comma()`.
- **Click** is the CLI framework (group-based command tree).
- **Explicit imports in `modules/__init__.py`** (since `e01def6`): `from .coinflip import (...)` with `__all__` — no longer star-imports there (star-imports remain in `utils/__init__.py` and consumers). Do not reintroduce shadowing.
- Output goes through `click.echo` (not `print`). **All modules echo in place**. Modules do **not** import other modules — each imports third-party libs directly (coinflip → `uwuipy`).
- Version lives in **two files** kept in sync: `pyproject.toml` + `src/kawa/__init__.py` (both `0.3.1`); runtime prefers `importlib.metadata.version("kawa")`.

## Patterns & Preferences

- Commits: conventional-commit with scopes — `feat(mc):`, `fix(ci):`, `chore(nix):`, `docs(readme):`, `refactor(cli):`.
- Kaomoji per family — **in flux**: committed code uses `(σ･ω･)σ` (coords) / `(σ≧∀≦)σ` (XP); uncommitted tree switches coords to `/ᐠ｡ꞈ｡ᐟ\`.
- Typo fixes: grep the whole tree (code + README + docs) in one pass (cf. "Expreience" → "Experience", 2026-10-16).
- **NO CODE COMMENTS** (user rule, 2026-10-16): zero `#` comments and zero docstrings except `cli.py` (Click `--help` text). Reason: the user writes their own comments to learn. Put details in the memory bank instead.

## Learnings & Project Insights

- `auto-click-auto` injects shell completion at the root `cli` group.
- Banner must stay in `kawa.spec` `datas`; loading uses `importlib.resources.files("kawa")`.
- `ruff check` + `ruff format --check` clean since the 2026-10-16 sweep (`f69ecbe` regressed I001+F401, fixed `151b8cc`). Ruff is now **blocking in CI** (PR #2).
- `json_tools.py` heuristic: file exists → read; else inline JSON; on failure path-like → "File not found", else "Invalid JSON".
- Ruff enforces `DTZ005` — coinflip uses `time.localtime().tm_hour`. Keep modules free of `noqa`.
- `coinflip(hour=None)` + `rng` injection lets tests force bias/events — reuse for future random/time features.
- **Coinflip crash (2026-10-17)**: nested-list `uwuify([pool])` broke uwuipy in ALL modes. Fixed `151b8cc`, superseded by `3056e31` (direct `uwu.uwuify(<string>)`). `f69ecbe` ("human slop code, lol") is user WIP — not a pattern.
- `secret` hits printed nothing before `151b8cc` (now plain `else`).
- **Pylance `reconfigure` false positive (2026-10-20)**: `sys.stdout` is typed `TextIO` (no `reconfigure` in stubs), so `hasattr` narrowing doesn't help. Fix: `getattr(stream, "reconfigure", None)` + `callable()` — no direct attribute access.
- **`except X, Y` is valid Python 3 (2026-10-20)**: comma form parses as tuple (`BUILD_TUPLE` + `CHECK_EXC_MATCH`, verified via `dis`); ruff format on this repo rewrites parenthesized `except (X, Y)` back to comma form. Keep comma form or `ruff format --check` fails CI.
- **Finite/overflow layering (2026-10-20)**: coords need BOTH `FiniteFloat` (parse-time) + `check_finite`/`check_overflow` (module-side: direct calls bypass Click, and `1e308*8 -> inf` overflows post-parse). Level/XP need neither (`int`: no NaN/inf, arbitrary precision).
