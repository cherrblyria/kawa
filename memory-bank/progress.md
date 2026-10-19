# Progress

## Current Status

**Code at 0.3.1** (`0a10611` == `origin/main`); tags `v0.3.1` (on `62a34a2`) and `v0.3.2` (on `b9fe2ac`) **both predate the code bump — version/tag mismatch**. Edge-case audit merged (PR #4). Suite: **58 `unittest` tests green on main** (minecraft 26, json 17, coinflip 8, uwuify 5, encoding 2). Ruff blocking + clean. **Tree: 58 run, all green** (drift fixed 2026-10-20). **Uncommitted working tree**: coordinate + XP cute-output rework (new kaomoji style, 4-message `BORDER_MESSAGE`, `rng` injection, `xp_for_level` renamed to `exp_for_level`), `cli.py` getattr-reconfigure fix, `coinflip.py` rng guards. README + 26 minecraft tests now assert new format (58/58 green). `ownt` tuple bug fixed (both use `rng.choice`).

## What Works

- [x] **`kawa mc ntow / ownt`** — ×8 / ÷8, `FiniteFloat` + finite/overflow guards, cute/json/plain, world-border egg. (Committed cute: `Nether: (x, z)  (σ･ω･)σ  Overworld: (X, Z)`.)
- [x] **`kawa mc lvxp / xplv`** — exact integer XP math + snap-back levels, `IntRange` bounds, easter eggs (21863, 2147483647).
- [x] **`kawa uwuify`** — per-word uwuification, cached `Uwuipy`, cute/json.
- [x] **`kawa json pretty`** — file / inline / stdin `-`; `-i/--indent 0..16`, `-s/--sort-keys`; hardened errors (broken symlink, dir, BOM, dup-key warnings, NaN/Infinity rejected, path-vs-JSON heuristic).
- [x] **`kawa coinflip`** — AM/PM bias (51/49 flip), uwuified `COINS_MESSAGES` fragments, own cached `Uwuipy`, `hour`+`rng` injectable; `--json` carries raw `message`, `--plain` is bare side.
- [x] **easter-egg events** — `EASTER_EGG_EVENTS`/`pick_event`: kawa 1/100 (uwuified), secret 1/100K (raw placeholder, lore pending). Cute-only, zero machine-mode rolls.
- [x] **Comment-free codebase** (user rule) — only `cli.py` docstrings remain. Document in bank instead.
- [x] **`--json` / `--plain`** — global decorator, leaf > group > cute, mutually exclusive, interspersed args, negative-safe via `MC_CONTEXT_SETTINGS`.
- [x] **58-test `unittest` suite** (PR #3 + audit; no pytest) — run in CI on ubuntu + windows.
- [x] **ruff blocking + clean** (PR #2 removed `continue-on-error`).
- [x] **Module decoupling** (`3056e31`) — modules never import modules.
- [x] **README** — human-slop trim (`b9fe2ac`): warning banner, short sections, Output-modes docs restored.
- [x] **`--version` / `--help` / completion / `python -m kawa` / uv workflow / Nix flake / PyInstaller binaries / release automation** — all working. Tags `v0.1.0`–`v0.3.2` exist.


## What's Left to Build

- Decide the uncommitted mc cute rework (coords AND xp/level, 4 borders, exp_for_level rename; tests + README updated) (`ownt` tuple bug, format change, README + 26 tests if kept).
- Resolve version/tag mismatch (code 0.3.1 vs tag v0.3.2).
- Additional "cute" tools (tagline is open-ended).
- Possible: `CHANGELOG.md`, PyPI publishing, man page, richer completion.
- Design the **lore/interactive coinflip event** with the user; replace `SECRET_PLACEHOLDER_MESSAGES` then.

## Known Issues / Quirks

- ~~UNCOMMITTED BUG~~ **fixed in tree**: both converters now use `rng.choice(BORDER_MESSAGE)` — still uncommitted.
- **Version/tag mismatch**: code 0.3.1, latest tag v0.3.2, both tags older than the bump commits.
- Resolved 2026-10-20 (tests updated + dead `test_xp_boundaries` revived + `__init__` import sort fixed): uncommitted format drift had tree printing `(x: ..) ... /ᐠ｡ꞈ｡ᐟ\`; README + tests expect `(σ･ω･)σ` style.
- "Expreience" typo fixed 2026-10-16 — grep whole tree for future typos.
- `no_dot_zero()`/`comma()` need numerics; version duplicated in two files (`cli.py` prefers installed metadata).

## Evolution of Project Decisions

1. **Argparse → Click** — current group/adapter architecture.
2. **Banner removed then restored** — keeper; asset pipeline stays intact.
3. **Shell completion via `auto-click-auto`** — keep the library.
4. **uv over pip/poetry** — `uv.lock` canonical; CI uses `uv`.
5. **uv2nix, `sourcePreference = "wheel"`** — Nix mirrors uv workspace.
6. **macOS runner fix** — `macos-15-intel` + `macos-15` split.
7. **Feature growth**: portal calc → level↔XP → `json pretty` (`5e7a004`) → `coinflip` (`a6e7140`) — thin-CLI + module-function pattern.
8. **Remote moved to SSH** (2026-10-16) — pushes prompt-free.
9. **Global output modes** (`78aade8`): `output_mode` decorator, leaf > group > cute; `json pretty` ignores mode.
10. **README simplification** (`acc29c9` + `b9fe2ac` human slop): open tagline, warning banner, Output-modes docs restored after deletion.
11. **Coinflip → easter-egg events** (`2e04c07`): `EASTER_EGG_EVENTS`/`pick_event`, kawa 1/100, 8 `COINS_MESSAGES` fragments (−61 lines).
12. **Messages uwuified** (`f69ecbe`, user WIP): return-value `uwuify` experiment — landed with all-mode crash + 2 ruff errors + silent secret.
13. **Repair** (`151b8cc`): pick-then-uwuify, `secret` prints, ruff fixed, README example refreshed.
14. **Decoupling** (`3056e31`, user decision): coinflip imports `uwuipy` directly — **modules never import modules**.
15. **Edge-case audit** (`6611d10`→`e01def6`, PR #4): exact XP ints, `FiniteFloat`, `IntRange` bounds, UTF-8 streams, cached `get_uwu`, `rng` injection, explicit `__all__`, JSON hardening, `MC_CONTEXT_SETTINGS` negatives.
16. **Real test suite** (PR #3 + audit): 58 `unittest` tests, CI on ubuntu + windows.
17. **Blocking ruff** (PR #2): `continue-on-error` removed.
18. **Non-negative XP/level** (PR #1): negatives rejected.
19. **0.3.1 code bump** (`2dd4856`/`d758923`/`9083713`) landed *after* tags v0.3.1/v0.3.2 — mismatch to resolve.

