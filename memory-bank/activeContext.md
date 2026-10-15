# Active Context

## Current Work Focus

Project is in a **stable, released state** at v0.2.0 on `main`. Latest commits: `99d37df docs(memory-bank): sync state + json pretty feature` and `5e7a004 feat(json): pretty print command` (both pushed to origin — remote URL switched to SSH, `git@github.com:cherrblyria/kawa.git`, since HTTPS had no credentials).

**In progress (uncommitted, 2026-10-16):** new `kawa coinflip` command (stdlib `random` + `time.localtime`, no new deps) — implemented in `src/kawa/modules/coinflip.py`, wired in `cli.py` and `modules/__init__.py`, README documented. Separate `HEADS_MESSAGES` / `TAILS_MESSAGES` pools (user will add more). AM (hour < 12) → Heads 51%/Tails 49%, PM → 49/51. Validated: ruff clean on new files, live CLI runs, and a 20k-iteration bias check per hour (AM ~51.6% heads, PM ~49.5%).

## Recent Changes (from git history)

- `99d37df` docs(memory-bank): sync state + json pretty feature (latest, pushed)
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

- Finish/commit `kawa coinflip` (in progress, uncommitted).
- User will extend the coinflip `HEADS_MESSAGES` / `TAILS_MESSAGES` pools.
- Add more "useless cute" tools (README hints at future features).
- Introduce a real test suite (currently only CI smoke tests; no pytest).
- Consider making ruff lint/format CI checks **blocking** (currently `continue-on-error: true`).

## Active Decisions & Considerations

- **Python 3.14 is a hard floor** (`requires-python = ">=3.14"`, `.python-version` = `3.14`, flake uses `pkgs.python314`). Code relies on `int.is_integer()` (3.12+) via `comma()`.
- **Click** is the CLI framework (group-based command tree).
- **Star-imports are the established pattern**: `from .utils import *`, `from .modules import *`, `from ..utils import *`. Follow it for consistency rather than switching to explicit imports.
- Output goes through `click.echo` (not `print`) — keep this convention.
- Version is declared in **two places** that must stay in sync: `pyproject.toml` (`version = "0.2.0"`) and `src/kawa/__init__.py` (`__version__ = "0.2.0"`); runtime display prefers `importlib.metadata.version("kawa")`.

## Patterns & Preferences

- Commit messages: conventional-commit style with scopes — `feat(mc):`, `fix(ci):`, `chore(nix):`, `docs(readme):`, `refactor(cli):`.
- Kaomoji differ per command family: `(σ･ω･)σ` for coordinates, `(σ≧∀≦)σ` for XP/level.
- The string "Expreience" (sic) appears consistently in code and README output examples — **do not silently "fix" it** without asking; it's either intentional voice or a known typo baked into docs.

## Learnings & Project Insights

- `auto-click-auto` provides `enable_click_shell_completion_option` which injects a completion option into a Click group — used at the root `cli` group.
- Banner asset must be listed in `kawa.spec` `datas` (`('src/kawa/assets', 'kawa/assets')`) for PyInstaller builds; loading uses `importlib.resources.files("kawa")`.
- CI smoke tests double as the only functional verification — always keep `kawa mc ntow/ownt` and `kawa uwuify` working.
- Full-repo `ruff check src` reports **8 pre-existing errors** in old files (`cli.py` unsorted imports/blind `except`/`dict()`, `minecraft.py` unsorted imports, `uwuify.py` enumerate misuse) — CI lint is `continue-on-error`, so these never blocked. Keep new files clean; don't "fix" old ones unless asked.
- `json_tools.py` error heuristic: file exists → read it; else parse arg as inline JSON; on failure, arg looks like a path (`.json` suffix or doesn't start with a JSON token) → "File not found", else "Invalid JSON" with line/column.
- Ruff (running with this project's effective ruleset) enforces `DTZ005` (`datetime.now()` without tz) — `coinflip.py` uses `time.localtime().tm_hour` instead, which is lint-clean and unambiguously "local time". Keep new modules free of `noqa`.
- `coinflip(hour=None)` takes an optional hour so bias can be tested by injection without touching the system clock — a good pattern for future random/time-based features.
