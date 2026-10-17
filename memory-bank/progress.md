# Progress

## Current Status

**v0.3.0 released** on `main` (tagged `v0.3.0`, 2026-10-16); everything after it is **unreleased**. As of 2026-10-17, HEAD is `34d4f42` (memory-bank decoupling sync) and **`main` is ahead of `origin/main` by 5 commits** (`f69ecbe` → `34d4f42` — not pushed). All healthy: coinflip works in all modes, `uwuify.py` echoes in place again (print-in-place restored), coinflip uses `uwuipy` directly (no module→module imports), `ruff check` + `ruff format --check` clean. Working tree clean. Multi-platform releases remain automated via tags.

## What Works

- [x] **`kawa mc ntow <x> <z>`** — Nether → Overworld coordinates (×8), cute output.
- [x] **`kawa mc ownt <x> <z>`** — Overworld → Nether coordinates (÷8).
- [x] **`kawa mc lvxp <level>`** — Level → Experience with piecewise formulas + easter eggs (max level 21863).
- [x] **`kawa mc xplv <xp>`** — Experience → Level (2-decimal output) + easter eggs (2147483647).
- [x] **`kawa uwuify <text...>`** — per-word uwuification via uwuipy.
- [x] **`kawa json pretty <source>`** (2026-10-15, committed `5e7a004`) — pretty-print JSON from a file path or raw string; stdlib `json`, no new deps. Options `-i/--indent` (default 4), `-s/--sort-keys`.
- [x] **`kawa coinflip`** (2026-10-16, `a6e7140`; reworked `acc29c9` → `2e04c07` → `f69ecbe`; repaired `151b8cc`; **decoupled `3056e31`**) — biased coinflip: AM (hour < 12) Heads 51%/Tails 49%, PM inverted; message is a random uwuified fragment from `COINS_MESSAGES` (8 punctuation fragments like `"! That's it"`), printed as `f"{side}{message}"`; uwuifies via its **own `Uwuipy()` instance** (`uwu.uwuify(<string>)`, not the uwuify module); stdlib `random` + `time.localtime`, no new deps. `hour` and `rng` injectable. Validated 2026-10-17: 150 flips across all modes, 0 crashes.
- [x] **coinflip easter-egg events** (originally `68c9ed1`; refactored `2e04c07`, 2026-10-17, both pushed except HEAD) — `SPECIAL_TIERS`/`pick_special_tier` → **`EASTER_EGG_EVENTS`/`pick_event`**: `kawa` (**1/100**, was 1/10K; `KAWA_MESSAGES`, 5 lines) and `secret` (1/100,000, `SECRET_PLACEHOLDER_MESSAGES`, 4 lines **pending the user's lore design**); a kawa hit replaces the flip and prints a uwuified Kawa message (no `Kawa!` prefix anymore); a `secret` hit prints its raw placeholder message (since `151b8cc`). Cute-mode-only — `--json`/`--plain` always plain heads/tails (zero event rolls). Old 20-line `HEADS_MESSAGES`/`TAILS_MESSAGES` pools were dropped in favor of `COINS_MESSAGES` fragments.
- [x] **Comment-free codebase** (2026-10-16, user rule) — all `#` comments and non-`cli.py` docstrings removed from every `.py` file; important content relocated here (special-tier semantics in `systemPatterns.md` #7). `cli.py` docstrings kept (Click `--help`). Rationale: user writes own comments to understand their code. Keep new code comment-free; document in memory bank instead.
- [x] **`--json` / `--plain` output modes** (2026-10-16, committed `78aade8`) — every command accepts both flags anywhere (leaf or group level); `output_mode` decorator in `cli.py`; modules take `mode="cute"` param. `json pretty` accepts the flags but ignores them (already JSON).
- [x] **ruff lint + format fully clean** (2026-10-16) — all 8 long-standing pre-existing lint errors fixed (blind `except` narrowed to `OSError`/`PackageNotFoundError`, import sorting, `dict()` → literal, redundant `pass` removed, enumerate misuse) plus a `ruff format` pass. Briefly regressed by `f69ecbe` (I001 + F401), **fixed again in `151b8cc`** — `ruff check src` and `ruff format --check src` both clean (10 files) as of 2026-10-17.
- [x] **uwuify module decoupling** (2026-10-17, `f69ecbe` → reverted `3056e31`) — `uwuify()` briefly became a return-value API so `coinflip` could compose with it; that module→module coupling caused the `151b8cc` crash. Final design: `uwuify.py` echoes in place like every other module, and `coinflip` imports `uwuipy` directly. **Convention: modules never import modules** (`systemPatterns.md` #8). `kawa uwuify` verified working in cute + `--json` modes.
- [x] **README trimmed** (`acc29c9`, 2026-10-16) — tagline now "A set of useless cute little CLI tools for... whatever."; **Output-modes section deleted** (the `--json`/`--plain` feature still exists in code), coinflip section shortened to "Flip a coin", features reordered (MC → Uwuify → Coinflip → JSON). Stale coinflip example replaced with real output in `151b8cc`; Output-modes section intentionally stays deleted (user decision).
- [x] **`kawa --version`** — ASCII banner + version (graceful fallback if asset missing).
- [x] **`--help` / `-h`** on all groups/commands (Click docstrings).
- [x] **Shell completion** via `auto-click-auto`.
- [x] **`python -m kawa`** entry point.
- [x] **uv-based dev workflow** with committed `uv.lock`.
- [x] **ruff lint + format** configured (`src = ["src"]`).
- [x] **Nix flake** packaging for 4 systems (uv2nix, wheel preference).
- [x] **PyInstaller single-file binaries** (`kawa.spec` with bundled assets).
- [x] **CI** (`.github/workflows/ci.yml`): ruff checks (non-blocking), smoke tests (blocking), `build-check` job that builds + runs the binary.
- [x] **Release automation** (`.github/workflows/release.yml`): tag `v*.*.*` → 4-platform binaries → GitHub Release with generated notes. Tags `v0.1.0`, `v0.2.0`, `v0.3.0` exist.

## What's Left to Build

- Additional "cute" tools — README tagline now open-ended ("...for... whatever.").
- A real automated test suite (pytest or similar); currently CI smoke tests are the only verification.
- ~~Make ruff lint/format CI checks **blocking** (they're `continue-on-error` today, so regressions can slip through).~~ — **safe to flip**: ruff check + format are clean as of `151b8cc`; just remove `continue-on-error` when ready.
- **Push** — `main` is ahead of `origin/main` by 5 commits (all post-v0.3.0, `f69ecbe` → `34d4f42`).
- ~~Decide whether to commit `.clinerules/` and `memory-bank/`~~ — **resolved**: both committed in `14da08b docs: initialize memory bank`.
- Possible: `CHANGELOG.md`, PyPI publishing (currently git-based installs only), man page, richer completion. (`--json` output — **done**, see "What Works".)

## Known Issues / Quirks

- **README drift** (`acc29c9`): Output-modes section deleted while `--json`/`--plain` still work — left as-is per user decision (coinflip example fixed in `151b8cc`).
- **Unpushed** — `main` is ahead of `origin/main` by 5 commits (`f69ecbe` → `34d4f42`).
- *(Resolved 2026-10-17 in `151b8cc`: coinflip crash in all modes — nested-list `uwuify` calls; silent `secret` branch; ruff I001/F401.)*
- **"Expreience" typo fixed → "Experience"** (2026-10-16, user request): corrected everywhere in one coordinated pass — CLI help docstrings, `minecraft.py` output strings, and README examples. Full-tree grep confirms no occurrences remain.
- Lint/format failures do not fail CI (by design or oversight — unconfirmed intent).
- `no_dot_zero()`/`comma()` require numeric input; any future command passing strings must format differently.
- `uwuify` re-instantiates randomness per word (new `Uwuipy()` each call is per-invocation; words share one instance) — output varies run to run by design.
- `.pyc` files from Python 3.11 **and** 3.14 coexist under `__pycache__/` (3.11 leftovers are ignored by `.gitignore`).
- Version duplication: `pyproject.toml` and `src/kawa/__init__.py` both say `0.3.0`; `cli.py` prefers installed metadata, falling back to `"unknown"` — misalignment possible if only one is bumped.

## Evolution of Project Decisions

1. **Argparse → Click** (`refactor(cli): click`) — established the current group/adapter architecture.
2. **Banner removed then restored** (`feat(cli): banner is back!`) — banner is a keeper; asset pipeline must stay intact.
3. **Shell completion added** via `auto-click-auto` rather than Click's built-in completion — keep using this library for consistency.
4. **uv adopted over pip/poetry** — `uv.lock` is canonical; all CI steps use `uv`.
5. **uv2nix for Nix packaging** with `sourcePreference = "wheel"` — Nix build mirrors the uv workspace.
6. **macOS runner fix** (`fix(ci): update macos runner`) — release matrix now uses `macos-15-intel` + `macos-15` for x86_64/arm64 split.
7. **Feature growth**: portal calculator first, then level↔XP calculator, then `kawa json pretty` (2026-10-15, first non-`mc`/non-text tool; lives in `src/kawa/modules/json_tools.py` under the root `json` group), then `kawa coinflip` (2026-10-16, first stdlib-`random` toy tool; `src/kawa/modules/coinflip.py`, top-level command) — future tools follow the thin-CLI + module-function pattern.
8. **Git remote moved to SSH** (2026-10-16): `origin` now `git@github.com:cherrblyria/kawa.git` because HTTPS had no stored credentials — pushes work without prompting.
9. **Global output modes** (2026-10-16, committed `78aade8`): `--json`/`--plain` added via a shared `output_mode` decorator applied to every group and leaf command — mode resolves as leaf flag > group flag > cute default, flags may appear anywhere Click allows (interspersed args). Modules keep print-in-place but now branch on `mode`. `json pretty` deliberately ignores the flags since its output is already JSON.
10. **README/tagline simplification** (2026-10-16, `acc29c9 docs: whatever`): tagline → "A set of useless cute little CLI tools for... whatever."; Output-modes docs removed from README, coinflip docs shortened to "Flip a coin", features reordered (MC → Uwuify → Coinflip → JSON); CLI help "Flip a biased coin" → "Flip a coin".
11. **Coinflip restructured into easter-egg events** (2026-10-17, `2e04c07 fix(coinflip): what`): `SPECIAL_TIERS` → `EASTER_EGG_EVENTS`, `pick_special_tier` → `pick_event`; kawa odds 1/10K → **1/100**; `HEADS_MESSAGES`/`TAILS_MESSAGES` (20 lines each) replaced by 8 short `COINS_MESSAGES` punctuation fragments; `KAWA_SECRET_PLACEHOLDER_MESSAGES` → `SECRET_PLACEHOLDER_MESSAGES` ("nutty the dev" voice); KAWA_MESSAGES down to 5 lines. Net −61 lines.
12. **Messages are uwuified** (2026-10-17, `f69ecbe`, user-authored WIP "human slop code, lol"): `uwuify()` switched to a return-value API so `coinflip` composes with it; cute output became `side + fragment` (no separator); `mc` easter-egg messages changed from `\n\n` to `\n`. Landed with defects (crash in all modes, 2 ruff errors, silent secret).
13. **Coinflip repair** (2026-10-17, `151b8cc`): pick the message *first*, then `uwuify([chosen])` — the old code passed nested lists to `uwuify()` (crash) and had no `secret` output branch (silent). Also fixed ruff `I001`/`F401` and refreshed the README coinflip example.
14. **Module decoupling** (2026-10-17, `3056e31`, user decision): reverted `uwuify()` to print-in-place and made `coinflip` import `uwuipy` directly — **modules never import modules; import the third-party lib instead**. Removes the coupling that caused #12/#13's bugs and restores the uniform print-in-place convention.
