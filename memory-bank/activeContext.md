# Active Context

## Current Work Focus

Project is in a **stable, released state** at v0.2.0 on `main`. Last commits were documentation polish (`docs(readme)`, `Update README.md`) and dependency hygiene (`chore(uv): remove unused dependency`).

As of 2026-10-15 the working tree is clean except for the **untracked `.clinerules/` directory** (contains the Cline memory-bank rule) — likely candidate for committing.

## Recent Changes (from git history)

- `5703e18` Update README.md (latest, matches workspace hash)
- `d0973e4` chore(uv): remove unused dependency
- `9222507` feat(mc): level ↔ xp calculator (`lvxp` / `xplv`)
- `6a69fac` feat: auto complete (via `auto-click-auto`)
- `aa4570c` feat(cli): banner is back!
- `54c8c68` chore(bump version): 0.2.0
- `0764012` refactor(cli): migrated to Click (from argparse presumably)

## Next Steps / Likely Future Work

- Commit `.clinerules/` (and `memory-bank/` once created) or add to `.gitignore`.
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
