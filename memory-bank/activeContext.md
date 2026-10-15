# Active Context

## Current Work Focus

Project is **stable and pushed**, `main` in sync with `origin/main` (2026-10-16). Latest shipped: **coinflip special-event tiers** (`68c9ed1`) and the **comment-free codebase rule** (`580e36d`) — both pushed, **post-v0.3.0 (unreleased)**.

`src/kawa/modules/coinflip.py` now has the `SPECIAL_TIERS` registry: **kawa** (1 in 10,000, `KAWA_MESSAGES`, 29 lines) and **secret** (1 in 100,000, `KAWA_SECRET_PLACEHOLDER_MESSAGES`, 3 placeholder lines). Cute-mode-only — `--json`/`--plain` never roll special tiers. The `secret` tier is a **placeholder awaiting the user's lore/interactive-event design** (user has "a lore" in progress; will provide details later — wire it via the tier registry, `tier["name"]` dispatch).

## Recent Changes (from git history)

- `580e36d` docs(memory-bank): special tiers pattern + comment-free rule (latest)
- `68c9ed1` feat(coinflip): cute-mode-only special event tiers
- `cfeb6a0` chore(uv): sync lockfile for 0.3.0 + memory-bank release status
- `bef2494` chore(bump version): 0.3.0
- `34bfae5` fix(cli): correct Expreience typo to Experience
- `87d1d79` docs(memory-bank): sync with shipped output modes + record typo fix
- `78aade8` feat(cli): global --json/--plain output modes
- `a6e7140` feat(coinflip): biased coinflip command
- `5e7a004` feat(json): pretty print command
- `14da08b` docs: initialize memory bank

## Next Steps / Likely Future Work

- Design + wire the **lore/interactive coinflip event** with the user (details pending from user); the `secret` tier's placeholder messages get replaced then. Extension point: `SPECIAL_TIERS` registry + `tier["name"]` dispatch in the cute branch.
- Next release: post-v0.3.0 commits (`68c9ed1` special tiers, `580e36d` docs) are pushed but unreleased — bump (both `pyproject.toml` and `src/kawa/__init__.py`) + tag when the user wants them shipped (e.g. `v0.4.0`).
- Add more "useless cute" tools (README hints at future features).
- Introduce a real test suite (currently only CI smoke tests; no pytest).
- Consider making ruff lint/format CI checks **blocking** (currently `continue-on-error: true`; codebase is now 100% clean, so safe to flip).

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
- **NO CODE COMMENTS** (user rule, 2026-10-16): the codebase is deliberately comment-free — zero `#` comments and zero docstrings anywhere except `cli.py` (Click uses command/group docstrings as `--help` text, so those stay). *Reason: the user writes their own comments to learn/verify they understand their own code.* Do not add comments to Python files; if a detail matters (math, TODOs, WIP, design intent, extension points), put it in the memory bank instead. `pick_special_tier`/`pretty_json` docstrings were removed as part of this sweep.

## Learnings & Project Insights

- `auto-click-auto` provides `enable_click_shell_completion_option` which injects a completion option into a Click group — used at the root `cli` group.
- Banner asset must be listed in `kawa.spec` `datas` (`('src/kawa/assets', 'kawa/assets')`) for PyInstaller builds; loading uses `importlib.resources.files("kawa")`.
- CI smoke tests double as the only functional verification — always keep `kawa mc ntow/ownt` and `kawa uwuify` working.
- Full-repo `ruff check src` was carrying **8 pre-existing errors** (unsorted imports, blind `except`, `dict()` call, unnecessary `pass`, enumerate misuse) — **all fixed 2026-10-16** (user request): safe fixes via `ruff check --fix`, BLE001 narrowed to `OSError` (banner read) and `PackageNotFoundError` (version lookup), plus a full `ruff format src` pass. `ruff check` + `ruff format --check` are now both fully clean — keep it that way.
- `json_tools.py` error heuristic: file exists → read it; else parse arg as inline JSON; on failure, arg looks like a path (`.json` suffix or doesn't start with a JSON token) → "File not found", else "Invalid JSON" with line/column.
- Ruff (running with this project's effective ruleset) enforces `DTZ005` (`datetime.now()` without tz) — `coinflip.py` uses `time.localtime().tm_hour` instead, which is lint-clean and unambiguously "local time". Keep new modules free of `noqa`.
- `coinflip(hour=None)` takes an optional hour so bias can be tested by injection without touching the system clock — a good pattern for future random/time-based features.
