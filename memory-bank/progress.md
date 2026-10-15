# Progress

## Current Status

**v0.2.0 released and stable** on `main` (latest commit `5703e18` "Update README.md"). All documented features work; CI passes with smoke tests + binary build check; multi-platform releases are automated via tags.

## What Works

- [x] **`kawa mc ntow <x> <z>`** — Nether → Overworld coordinates (×8), cute output.
- [x] **`kawa mc ownt <x> <z>`** — Overworld → Nether coordinates (÷8).
- [x] **`kawa mc lvxp <level>`** — Level → Experience with piecewise formulas + easter eggs (max level 21863).
- [x] **`kawa mc xplv <xp>`** — Experience → Level (2-decimal output) + easter eggs (2147483647).
- [x] **`kawa uwuify <text...>`** — per-word uwuification via uwuipy.
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
- Make ruff lint/format CI checks **blocking** (they're `continue-on-error` today, so regressions can slip through).
- Decide whether to commit `.clinerules/` (untracked) and the new `memory-bank/` directory, or gitignore them.
- Possible: `CHANGELOG.md`, PyPI publishing (currently git-based installs only), man page/`--json` output, richer completion.

## Known Issues / Quirks

- **"Expreience"** (sic) typo is baked into CLI help text, module output, and README examples — consistent everywhere. Treat as known quirk; changing it is a coordinated docs+code change.
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
7. **Feature growth**: portal calculator first, then level↔XP calculator — the `mc` group is the designated home for future Minecraft tools.
