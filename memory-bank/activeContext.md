# Active Context

## Current Work Focus

Project is in a **stable, released state** at **v0.3.0** on `main`, tagged `v0.3.0` and **pushed to origin** (2026-10-16). The tag triggers the release workflow (4-platform binaries + GitHub Release). Latest commits: `bef2494 chore(bump version): 0.3.0`, `34bfae5 fix(cli): correct Expreience typo to Experience`, `87d1d79 docs(memory-bank): sync...`. Working tree clean; `main` in sync with `origin/main`.

Shipped since `origin/main`: biased `kawa coinflip`, global `--json`/`--plain` output modes on every command, full ruff lint+format cleanup, plus `kawa json pretty` (already pushed).

## Recent Changes (from git history)

- `d71ed5f` docs(memory-bank): output modes + ruff cleanup (latest, local only)
- `78aade8` feat(cli): global --json/--plain output modes (local only; includes ruff cleanup + format pass)
- `c7d84de` docs(memory-bank): coinflip feature + push state (local only)
- `a6e7140` feat(coinflip): biased coinflip command (local only)
- `99d37df` docs(memory-bank): sync state + json pretty feature
- `5e7a004` feat(json): pretty print command
- `14da08b` docs: initialize memory bank
- `5703e18` Update README.md
- `d0973e4` chore(uv): remove unused dependency
- `9222507` feat(mc): level ↔ xp calculator (`lvxp` / `xplv`)
- `6a69fac` feat: auto complete (via `auto-click-auto`)
- `aa4570c` feat(cli): banner is back!
- `54c8c68` chore(bump version): 0.2.0
- `0764012` refactor(cli): migrated to Click (from argparse presumably)

## Next Steps / Likely Future Work

- Push the 4 local commits to origin; consider a `0.3.0` bump (both `pyproject.toml` and `src/kawa/__init__.py`) + `v0.3.0` tag to cut a release with all new features. — **done 2026-10-16**: v0.3.0 tagged & pushed; release workflow triggered (verify binaries on the Releases page — `gh` CLI unavailable locally).
- User will extend the coinflip `HEADS_MESSAGES` / `TAILS_MESSAGES` pools.
- Add more "useless cute" tools (README hints at future features).
- Introduce a real test suite (currently only CI smoke tests; no pytest).
- Consider making ruff lint/format CI checks **blocking** (currently `continue-on-error: true`).

## Active Decisions & Considerations

- **Python 3.14 is a hard floor** (`requires-python = ">=3.14"`, `.python-version` = `3.14`, flake uses `pkgs.python314`). Code relies on `int.is_integer()` (3.12+) via `comma()`.
- **Click** is the CLI framework (group-based command tree).
- **Star-imports are the established pattern**: `from .utils import *`, `from .modules import *`, `from ..utils import *`. Follow it for consistency rather than switching to explicit imports.
- Output goes through `click.echo` (not `print`) — keep this convention.
- Version is declared in **two places** that must stay in sync: `pyproject.toml` (`version = "0.3.0"`) and `src/kawa/__init__.py` (`__version__ = "0.3.0"`); runtime display prefers `importlib.metadata.version("kawa")`.

## Patterns & Preferences

- Commit messages: conventional-commit style with scopes — `feat(mc):`, `fix(ci):`, `chore(nix):`, `docs(readme):`, `refactor(cli):`.
- Kaomoji differ per command family: `(σ･ω･)σ` for coordinates, `(σ≧∀≦)σ` for XP/level.
- The "Expreience" → "Experience" typo was fixed everywhere in a single coordinated change (2026-10-16, user request) — for future typos, grep the whole tree (code + README + docs) and fix all occurrences together.

## Learnings & Project Insights

- `auto-click-auto` provides `enable_click_shell_completion_option` which injects a completion option into a Click group — used at the root `cli` group.
- Banner asset must be listed in `kawa.spec` `datas` (`('src/kawa/assets', 'kawa/assets')`) for PyInstaller builds; loading uses `importlib.resources.files("kawa")`.
- CI smoke tests double as the only functional verification — always keep `kawa mc ntow/ownt` and `kawa uwuify` working.
- Full-repo `ruff check src` was carrying **8 pre-existing errors** (unsorted imports, blind `except`, `dict()` call, unnecessary `pass`, enumerate misuse) — **all fixed 2026-10-16** (user request): safe fixes via `ruff check --fix`, BLE001 narrowed to `OSError` (banner read) and `PackageNotFoundError` (version lookup), plus a full `ruff format src` pass. `ruff check` + `ruff format --check` are now both fully clean — keep it that way.
- `json_tools.py` error heuristic: file exists → read it; else parse arg as inline JSON; on failure, arg looks like a path (`.json` suffix or doesn't start with a JSON token) → "File not found", else "Invalid JSON" with line/column.
- Ruff (running with this project's effective ruleset) enforces `DTZ005` (`datetime.now()` without tz) — `coinflip.py` uses `time.localtime().tm_hour` instead, which is lint-clean and unambiguously "local time". Keep new modules free of `noqa`.
- `coinflip(hour=None)` takes an optional hour so bias can be tested by injection without touching the system clock — a good pattern for future random/time-based features.
