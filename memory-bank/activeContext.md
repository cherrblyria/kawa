# Active Context

## Current Work Focus

Project is **healthy again** (2026-10-17): `151b8cc` repaired the breakage `f69ecbe` introduced — pick-then-uwuify, `secret` event prints, ruff `I001`/`F401` fixed, README coinflip example refreshed. **HEAD `151b8cc` is unpushed — `main` is 2 ahead of `origin/main`** (`f69ecbe`, `151b8cc`), both post-v0.3.0/unreleased. `ruff check` + `ruff format --check` clean. Validated: 150 flips across all modes (0 crashes), forced `kawa`/`secret` events via `rng` injection, machine-mode zero-roll proof (`rng` that raises if called), full command smoke.

`src/kawa/modules/coinflip.py` current shape: `EASTER_EGG_EVENTS`/`pick_event` (kawa **1/100**, secret **1/100,000**), pools `COINS_MESSAGES` (8 punctuation fragments), `KAWA_MESSAGES` (5 lines), `SECRET_PLACEHOLDER_MESSAGES` (4 lines, "nutty the dev" placeholder voice). Messages: **pick first, then `uwuify([chosen])`** — `uwuify()` takes a flat list and returns one joined string, so a whole pool must never be passed. Only the `kawa` event is uwuified; `secret` prints raw. The `secret` event remains a **placeholder awaiting the user's lore/interactive-event design** (wire via `EASTER_EGG_EVENTS` + `event["name"]` dispatch).

## Recent Changes (from git history)

- `151b8cc` fix(coinflip): pick-then-uwuify messages + print secret event — **HEAD, unpushed**
- `f69ecbe` feat(coinflip): uwuify coinflip (human slop code, lol)
- `2e04c07` fix(coinflip): what — `EASTER_EGG_EVENTS` refactor
- `acc29c9` docs: whatever — README trim + new tagline
- `90376f2` docs(memory-bank): sync post-v0.3.0 state
- `580e36d` docs(memory-bank): special tiers pattern + comment-free rule
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

- **Push `f69ecbe` + `151b8cc`** — `main` is 2 commits ahead of `origin/main`.
- Optional: the README still has no Output-modes docs (user decision 2026-10-17 — keep deleted unless they change their mind).
- Design + wire the **lore/interactive coinflip event** with the user (details pending from user); `secret`'s `SECRET_PLACEHOLDER_MESSAGES` get replaced then. Extension point: `EASTER_EGG_EVENTS` registry + `event["name"]` dispatch in the cute branch.
- Next release: everything since `v0.3.0` (`68c9ed1`, `580e36d`, `90376f2`, `acc29c9`, `2e04c07`, `f69ecbe`, `151b8cc` + docs) is unreleased — bump (both `pyproject.toml` and `src/kawa/__init__.py`) + tag when the user wants it shipped (e.g. `v0.4.0`).
- Add more "useless cute" tools (README tagline now open-ended: "...for... whatever.").
- Introduce a real test suite (currently only CI smoke tests; no pytest — and CI does **not** exercise `coinflip`; worth adding it to the smoke list now that it works).
- Consider making ruff lint/format CI checks **blocking** (currently `continue-on-error: true`) — ruff is clean as of `151b8cc`, so safe to flip.

## Active Decisions & Considerations

- **Python 3.14 is a hard floor** (`requires-python = ">=3.14"`, `.python-version` = `3.14`, flake uses `pkgs.python314`). Code relies on `int.is_integer()` (3.12+) via `comma()`.
- **Click** is the CLI framework (group-based command tree).
- **Star-imports are the established pattern**: `from .utils import *`, `from .modules import *`, `from ..utils import *`. Follow it for consistency rather than switching to explicit imports.
- Output goes through `click.echo` (not `print`) — keep this convention. Since `f69ecbe`, `modules/uwuify.py` **returns** its result instead of echoing: the `uwuify` CLI command echoes in `cli.py`, and `coinflip` composes with it internally (`from .uwuify import uwuify`). `mc`/`json_tools`/`coinflip` still echo in place. New reusable helpers should prefer returning; leaf commands echo.
- Version is declared in **two places** that must stay in sync: `pyproject.toml` (`version = "0.3.0"`) and `src/kawa/__init__.py` (`__version__ = "0.3.0"`); runtime display prefers `importlib.metadata.version("kawa")`.

## Patterns & Preferences

- Commit messages: conventional-commit style with scopes — `feat(mc):`, `fix(ci):`, `chore(nix):`, `docs(readme):`, `refactor(cli):`.
- Kaomoji differ per command family: `(σ･ω･)σ` for coordinates, `(σ≧∀≦)σ` for XP/level.
- The "Expreience" → "Experience" typo was fixed everywhere in a single coordinated change (2026-10-16, user request) — for future typos, grep the whole tree (code + README + docs) and fix all occurrences together.
- **NO CODE COMMENTS** (user rule, 2026-10-16): the codebase is deliberately comment-free — zero `#` comments and zero docstrings anywhere except `cli.py` (Click uses command/group docstrings as `--help` text, so those stay). *Reason: the user writes their own comments to learn/verify they understand their own code.* Do not add comments to Python files; if a detail matters (math, TODOs, WIP, design intent, extension points), put it in the memory bank instead. `pick_special_tier`/`pretty_json` docstrings were removed as part of this sweep (`pick_special_tier` was later renamed `pick_event` in `2e04c07`).

## Learnings & Project Insights

- `auto-click-auto` provides `enable_click_shell_completion_option` which injects a completion option into a Click group — used at the root `cli` group.
- Banner asset must be listed in `kawa.spec` `datas` (`('src/kawa/assets', 'kawa/assets')`) for PyInstaller builds; loading uses `importlib.resources.files("kawa")`.
- CI smoke tests double as the only functional verification — always keep `kawa mc ntow/ownt` and `kawa uwuify` working.
- Full-repo `ruff check src` was carrying **8 pre-existing errors** (unsorted imports, blind `except`, `dict()` call, unnecessary `pass`, enumerate misuse) — **all fixed 2026-10-16** (user request): safe fixes via `ruff check --fix`, BLE001 narrowed to `OSError` (banner read) and `PackageNotFoundError` (version lookup), plus a full `ruff format src` pass. `ruff check` + `ruff format --check` were 100% clean after that — **regressed 2026-10-17**: `f69ecbe` introduced 2 new `ruff check` errors (`I001` unsorted imports in `coinflip.py`, `F401` unused `click` in `uwuify.py`); `ruff format --check src` still passes (10 files) — both errors fixed again in `151b8cc` (import sorted into the local block; unused `click` removed).
- `json_tools.py` error heuristic: file exists → read it; else parse arg as inline JSON; on failure, arg looks like a path (`.json` suffix or doesn't start with a JSON token) → "File not found", else "Invalid JSON" with line/column.
- Ruff (running with this project's effective ruleset) enforces `DTZ005` (`datetime.now()` without tz) — `coinflip.py` uses `time.localtime().tm_hour` instead, which is lint-clean and unambiguously "local time". Keep new modules free of `noqa`.
- `coinflip(hour=None)` takes an optional hour so bias can be tested by injection without touching the system clock — a good pattern for future random/time-based features.
- **Coinflip breakage diagnosis (2026-10-17)**: `uwuify([COINS_MESSAGES])` (and `uwuify([event["messages"]])`) wrap the pool in a *second* list, so `uwuify()`'s loop hands uwuipy a `list` which dies on `_msg.split(" ")` → `AttributeError: 'list' object has no attribute 'split'`. The `else` branch runs for **all** modes before output, so even `--plain`/`--json` crash — `coinflip` is 100% broken, not just cute mode. CI stays green because its smoke tests only cover `ntow`/`ownt`/`uwuify`. (**Fixed in `151b8cc`**: pick the message first, then `uwuify([chosen])` — one fragment at a time; a whole pool must never be passed since `uwuify` returns one joined string.)
- Cute-branch gap in `coinflip()`: output branches are `event is None` → normal flip, `event["name"] == "kawa"` → message; a **`secret` hit falls through and prints nothing** (no crash: `side` is only referenced in branches unreachable in machine modes, since `pick_event` returns `None` there). (**Fixed in `151b8cc`**: the branch collapsed to a plain `else` — any event prints its message.)
- `f69ecbe` is self-described "human slop code, lol" — the user wrote it by hand. Treat it as a WIP snapshot, **not** a pattern to imitate (nested-list `uwuify` call and the unused-import fallout are defects, not conventions). Superseded by the `151b8cc` repair.
