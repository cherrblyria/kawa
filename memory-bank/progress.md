# Progress

## Current Status

**v0.2.0 released and stable** on `main` (latest commit `d71ed5f` "docs(memory-bank): output modes + ruff cleanup"; prior `78aade8` "feat(cli): global --json/--plain output modes"). **Working tree clean**; `main` ahead of `origin/main` by **4** (`a6e7140`, `c7d84de`, `78aade8`, `d71ed5f`) — committed locally but **not pushed**. All documented features work; ruff lint + format are 100% clean; CI passes with smoke tests + binary build check; multi-platform releases are automated via tags.

## What Works

- [x] **`kawa mc ntow <x> <z>`** — Nether → Overworld coordinates (×8), cute output.
- [x] **`kawa mc ownt <x> <z>`** — Overworld → Nether coordinates (÷8).
- [x] **`kawa mc lvxp <level>`** — Level → Experience with piecewise formulas + easter eggs (max level 21863).
- [x] **`kawa mc xplv <xp>`** — Experience → Level (2-decimal output) + easter eggs (2147483647).
- [x] **`kawa uwuify <text...>`** — per-word uwuification via uwuipy.
- [x] **`kawa json pretty <source>`** (2026-10-15, committed `5e7a004`) — pretty-print JSON from a file path or raw string; stdlib `json`, no new deps. Options `-i/--indent` (default 4), `-s/--sort-keys`.
- [x] **`kawa coinflip`** (2026-10-16, committed `a6e7140`) — biased coinflip: `Heads|Tails! <random message>`; separate `HEADS_MESSAGES`/`TAILS_MESSAGES` pools in `src/kawa/modules/coinflip.py`; AM (hour < 12) Heads 51%/Tails 49%, PM inverted; stdlib `random` + `time.localtime`, no new deps. `hour` param injectable for bias testing.
- [x] **`--json` / `--plain` output modes** (2026-10-16, committed `78aade8`) — every command accepts both flags anywhere (leaf or group level); `output_mode` decorator in `cli.py`; modules take `mode="cute"` param. `json pretty` accepts the flags but ignores them (already JSON).
- [x] **ruff lint + format fully clean** (2026-10-16) — all 8 long-standing pre-existing lint errors fixed (blind `except` narrowed to `OSError`/`PackageNotFoundError`, import sorting, `dict()` → literal, redundant `pass` removed, enumerate misuse) plus a `ruff format` pass. `ruff check src` and `ruff format --check src` both pass with 0 issues.
- [x] **`kawa --version`** — ASCII banner + version (graceful fallback if asset missing).
- [x] **`--help` / `-h`** on all groups/commands (Click docstrings).
- [x] **Shell completion** via `auto-click-auto`.
- [x] **`python -m kawa`** entry point.
- [x] **uv-based dev workflow** with committed `uv.lock`.
- [x] **ruff lint + format** configured (`src = ["src"]`).
- [x] **Nix flake** packaging for 4 systems (uv2nix, wheel preference).
- [x] **PyInstaller single-file binaries** (`kawa.spec` with bundled assets).
- [x] **CI** (`.github/workflows/ci.yml`): ruff checks (non-blocking), smoke tests (blocking), `build-check` job that builds + runs the binary.
- [x] **Release automation** (`.github/workflows/release.yml`): tag `v*.*.*` → 4-platform binaries → GitHub Release with generated notes. Tags `v0.1.0`, `v0.2.0` exist.

## What's Left to Build

- Additional "cute" tools — README explicitly leaves the door open ("...that's it (for now)").
- A real automated test suite (pytest or similar); currently CI smoke tests are the only verification.
- ~~Make ruff lint/format CI checks **blocking** (they're `continue-on-error` today, so regressions can slip through).~~ — now much safer to flip: codebase is 100% lint + format clean as of 2026-10-16; just remove `continue-on-error` when ready.
- ~~Decide whether to commit `.clinerules/` and `memory-bank/`~~ — **resolved**: both committed in `14da08b docs: initialize memory bank`.
- Possible: `CHANGELOG.md`, PyPI publishing (currently git-based installs only), man page, richer completion. (`--json` output — **done**, see "What Works".)

## Known Issues / Quirks

- **"Expreience" typo fixed → "Experience"** (2026-10-16, user request): corrected everywhere in one coordinated pass — CLI help docstrings, `minecraft.py` output strings, and README examples. Full-tree grep confirms no occurrences remain.
- Lint/format failures do not fail CI (by design or oversight — unconfirmed intent).
- `no_dot_zero()`/`comma()` require numeric input; any future command passing strings must format differently.
- `uwuify` re-instantiates randomness per word (new `Uwuipy()` each call is per-invocation; words share one instance) — output varies run to run by design.
- `.pyc` files from Python 3.11 **and** 3.14 coexist under `__pycache__/` (3.11 leftovers are ignored by `.gitignore`).
- Version duplication: `pyproject.toml` and `src/kawa/__init__.py` both say `0.2.0`; `cli.py` prefers installed metadata, falling back to `"unknown"` — misalignment possible if only one is bumped.

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
