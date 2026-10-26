# Active Context

## Current Work Focus

Edge-case audit merged (PR #4), follow-ups landed, **command aliases shipped**. **HEAD at write time: `b937658` (alias feature) + this sync = local `main` ahead of `origin/main` by 3 (UNPUSHED)**; working tree clean. Suite **58 `unittest` tests green** (re-run 2026-10-20 after aliases: minecraft 26, json 17, coinflip 8, uwuify 5, encoding 2; 17.5s) via `python -m unittest discover -s tests -v` in CI (ubuntu + windows). Ruff blocking + clean.

**Command aliases are COMMITTED** (`b937658 feat(cli): command aliases via click-aliases`): new dep `click-aliases>=1.0.7` (pyproject + uv.lock); `ClickAliasedGroup` on the root `cli` group and the `minecraft` group. Descriptive canonical names with legacy/short aliases — `minecraft`=`mc`, `nether`=`ntow`/`nt`, `overworld`=`ownt`/`ow`, `level`=`lvxp`/`lv`, `xp`=`xplv` (its aliases list redundantly re-lists `xp`, harmless), `uwuify`=`uwu`, `coinflip`=`cf`. Old invocations (`kawa mc ntow …`) still work, so README examples/tests stay valid. `json`→`pretty` stays a plain group — no aliases there.

**The cute-output rework is COMMITTED** (`a8f696f fix(mc): new cute output style, rng injection, exp_for_level rename` + `e18e992 docs(readme): refresh minecraft examples`): kaomoji coords `/ᐠ｡ꞈ｡ᐟ\`, xp/level `/ᐠ｡‸｡ᐟ\`, 4-message `BORDER_MESSAGE` list, `rng` injection, `xp_for_level` → `exp_for_level`, `cli.py` `getattr`+`callable` reconfigure fix, README examples refreshed, tests assert the new format. The old `(σ･ω･)σ` style is gone from the whole tree (grep-clean).

**Version/tag mismatch resolved**: code `0.3.1` (pyproject + `__init__`), tags are `v0.1.0`–`v0.3.1` with **`v0.3.1` on `0a10611`** (the version-bump merge); the stray `v0.3.2` tag no longer exists. Code and latest tag agree.

Conventions: `run_*` names (`run_coinflip`, `run_uwuify`) with explicit `__all__`; lazy cached `Uwuipy` via `functools.cache get_uwu()` per module; `rng` injection in coinflip + minecraft converters; `click.IntRange` bounds (level ≤ 1e9, xp ≤ 1e18, indent 0..16); `--json`+`--plain` → `UsageError`; UTF-8 streams forced at startup via `getattr`/`callable`; `FiniteFloat` rejects NaN/inf; `MC_CONTEXT_SETTINGS` on `minecraft` leaves (alias `mc`) for negative numbers.

Coinflip shape: `EASTER_EGG_EVENTS`/`pick_event` (kawa 1/100, secret 1/100K), `COINS_MESSAGES` (8 fragments), `KAWA_MESSAGES` (5), `SECRET_PLACEHOLDER_MESSAGES` (4, "nutty the dev" voice). No dependency on `modules/uwuify.py` (`3056e31`). Only `kawa` is uwuified; `secret` prints raw and awaits the user's lore design.

## Recent Changes (newest first)

- this sync — docs(memory-bank): alias rework sync
- `b937658` feat(cli): command aliases via click-aliases — canonical rename + back-compat aliases (current HEAD)
- `1c60f88` docs(memory-bank): sync committed rework + version/tag alignment
- `e18e992` docs(readme): refresh minecraft examples to new cute output style (was == origin/main)
- `a8f696f` fix(mc): new cute output style, rng injection, exp_for_level rename — the formerly-uncommitted rework (incl. CLI UTF-8 getattr fix) **committed**
- `0a10611` merge main (tag **v0.3.1** — the version-bump merge)
- `9083713` + `2dd4856` + `d758923` bump code to 0.3.1
- `b9fe2ac` docs(readme): human slop — warning banner, trimmed sections, Output-modes restored
- `c74297a` Merge PR #4 `fix/edge-cases` (`6611d10` mc → `9ef1b2d` json → `adc030f` UTF-8 → `e01def6` internals → `0a8543a` docs/sync)
- `f9f39ad` Merge PR #3 test suite; `3eafe87` Merge PR #2 blocking ruff; `15d3f89` Merge PR #1 non-negative XP/level
- `62a34a2` docs(readme): sort
- Older: `34d4f42` memory-bank sync; `3056e31` coinflip→uwuipy direct; `151b8cc` coinflip repair; `f69ecbe` uwuify-coinflip WIP; `2e04c07` EASTER_EGG_EVENTS refactor; `acc29c9` README trim

## Next Steps / Likely Future Work

- Design the **lore/interactive coinflip event** with the user; replace `SECRET_PLACEHOLDER_MESSAGES` then.
- Add more "useless cute" tools; possible `CHANGELOG.md`, PyPI publishing, man page.
- **Push local `main`** — 3 unpushed commits (`1c60f88`, `b937658`, this sync).
- Ship next release (0.3.2?): HEAD sits 5 commits past tag `v0.3.1` (cute rework, README refresh, 2 bank syncs, alias feature).


## Active Decisions & Considerations

- **Python 3.14 is a hard floor** (`requires-python = ">=3.14"`, `.python-version` = `3.14`, flake uses `pkgs.python314`). Code relies on `int.is_integer()` (3.12+) via `comma()`.
- **Click** is the CLI framework (group-based command tree).
- **Explicit imports in `modules/__init__.py`** (since `e01def6`): `from .coinflip import (...)` with `__all__` — no longer star-imports there (star-imports remain in `utils/__init__.py` and consumers). Do not reintroduce shadowing.
- Output goes through `click.echo` (not `print`). **All modules echo in place**. Modules do **not** import other modules — each imports third-party libs directly (coinflip → `uwuipy`).
- Version lives in **two files** kept in sync: `pyproject.toml` + `src/kawa/__init__.py` (both `0.3.1`); runtime prefers `importlib.metadata.version("kawa")`.

## Patterns & Preferences

- Commits: conventional-commit with scopes — `feat(mc):`, `fix(ci):`, `chore(nix):`, `docs(readme):`, `refactor(cli):`.
- CLI naming: descriptive canonical names + short/legacy aliases via `click-aliases` (`ClickAliasedGroup`); never break old invocations — a rename must keep the old name as an alias.
- Kaomoji per family (committed in `a8f696f`): coords `/ᐠ｡ꞈ｡ᐟ\`, xp/level `/ᐠ｡‸｡ᐟ\`. The old `(σ･ω･)σ` / `(σ≧∀≦)σ` style is fully replaced — no `σ` remains in `src/`, `README.md`, or `tests/`.
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


Storage converter implementation is in progress on `feat/mc-storage-converter`. Added `minecraft`/`mc` leaf commands `item`, `stack`, and `shulker`/`sb`, exact integer item pivot math, optional custom stack size and large-chest mode, cute/plain/JSON output, breakdowns for non-whole conversions, README coverage, and a CI smoke command. Added `tests/test_minecraft_storage_cli.py` (8 test methods). The remote GitHub edits have **not yet been run locally**; `uv sync --dev`, unittest, Ruff checks/formatting, and full manual matrix remain required before declaring the branch green. Stack size intentionally has no upper bound; formatting failures from Python's integer digit limit are translated to `click.BadParameter("result too large")`.
