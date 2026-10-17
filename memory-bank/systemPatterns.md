# System Patterns

## Architecture Overview

Small layered Click CLI with a strict split between command wiring, feature logic, and formatting:

```text
src/kawa/
├── __init__.py          # __version__ = "0.3.0"
├── __main__.py          # python -m kawa → cli()
├── cli.py               # Click command tree (thin; delegates to modules)
├── modules/             # Feature logic (echoes or returns; see #8)
│   ├── __init__.py      # from .minecraft import *; from .uwuify import *; from .coinflip import *; from .json_tools import *
│   ├── minecraft.py     # coordinate + XP/level math
│   ├── uwuify.py        # uwuipy wrapper — returns the result (no echo) since f69ecbe
│   ├── coinflip.py      # biased coinflip + easter-egg events; uwuifies its messages
│   └── json_tools.py    # JSON pretty printer
├── utils/               # Pure formatting helpers
│   ├── __init__.py      # from .format import *
│   └── format.py        # no_dot_zero(), comma()
└── assets/
    └── banner.txt       # ASCII banner for --version
```

## Component Relationships

```text
cli.py ──imports──▶ modules/ ──imports──▶ utils/
   │                    │
   └── assets/banner.txt (via importlib.resources)
   └── importlib.metadata.version("kawa")
```

- **`cli.py`** defines the root group `cli` (with banner version option + shell completion), subgroup `mc`, and top-level commands `uwuify`, `coinflip`, plus the `json` group. Each command is a thin adapter: parse args with Click types (`float`/`int`/`nargs=-1`), call the module function. Every group and leaf command is wrapped by the shared `output_mode` decorator which attaches `--json`/`--plain` flags.
- **`modules/`** own the domain math and all user-facing output. `minecraft.py`, `coinflip.py` and `json_tools.py` print directly with `click.echo`; `uwuify.py` **returns** its string/JSON instead (since `f69ecbe`) so `coinflip` can compose with it — the `uwuify` CLI command echoes the return value in `cli.py`. Modules may import sibling modules (`coinflip` → `uwuify`).
- **`utils/`** are pure formatting functions shared by modules.

## Key Technical Decisions

1. **Click groups over subparsers**: `cli` → `mc` → `{ntow, ownt, lvxp, xplv}`; `uwuify` sits at the root. Help text lives in docstrings.
2. **Star-import export pattern**: each package's `__init__.py` re-exports with `from .module import *`; consumers do `from .modules import *`. Convention over explicitness.
3. **Print-in-place, not return** (default; nuanced by #8): module functions perform their own `click.echo` — except `uwuify()`, which returns so it can be composed with. New commands should follow the standard shape (logic + output in the module, wiring in `cli.py`); only make a helper return when other modules need its value.
4. **Defensive asset/metadata loading**: banner and version are loaded in `try/except` with graceful fallbacks (`"Oops!, seem like banner is missing..."`, `"unknown"`).
5. **Float-typed coordinate args**: Click casts `x`/`z` to `float` so `no_dot_zero()` can call `.is_integer()`. XP/level args are `int` (Python 3.12+ ints also have `.is_integer()`, relied upon by `comma()`).
6. **Global output modes via decorator** (2026-10-16): `output_mode` in `cli.py` adds `--json`/`--plain` to every group and leaf command. Resolution: leaf flag > nearest ancestor group flag > `"cute"` default (`--json` wins if both given on the same level). The mode travels via Click's parent-`ctx.obj` chain, and each wrapper's callback receives a `mode` kwarg it forwards to the module function. Modules branch `mode == "json"` / `"plain"` / else cute. `json pretty` is intentionally mode-agnostic (already JSON).
7. **Coinflip easter-egg events** (`EASTER_EGG_EVENTS` in `coinflip.py`; originally `SPECIAL_TIERS`/`pick_special_tier`, renamed & simplified in `2e04c07`, 2026-10-17): ordered registry of rare outcomes; each event is `{name, chance, messages}` and gets its own independent roll, first hit wins (**kawa** 1/100 → **secret** 1/100,000 → normal biased flip). The kawa odds were tightened from the original 1/10,000 at rename time. Because rolls are sequential & independent, the effective secret chance is (1 − 1/100) × 1/100,000 (intentional). A hit replaces the coin flip entirely. **Extension point: append to `EASTER_EGG_EVENTS` — flip logic never changes**; future interactive/lore events can add fields (e.g. a handler) and switch on `event["name"]` in the cute branch. Two hard rules: **(a) cute-mode only** — `pick_event` returns `None` immediately for any non-cute mode, so `--json`/`--plain` make *zero* random rolls for events and always emit deterministic heads/tails; **(b) `rng` injection** — `pick_event(mode, rng=None)` / `coinflip(..., rng=None)` take a callable instead of calling `random.random` directly, so tests and future interactive events can force an event. The `secret` event's messages (`SECRET_PLACEHOLDER_MESSAGES`, formerly `KAWA_SECRET_PLACEHOLDER_MESSAGES`) stay placeholders until the user's lore design lands. Star-import caveat: `kawa.modules.coinflip` resolves to the *function* (star-export shadows the submodule) — tests must reach the module via `sys.modules["kawa.modules.coinflip"]`. (This entry preserves knowledge that used to live in code comments — removed 2026-10-16 by user preference.)
8. **`uwuify` returns, callers echo** (`f69ecbe`, 2026-10-17): `modules/uwuify.py` switched from `click.echo`-in-place to returning the string (or JSON string); `cli.py` wraps the `uwuify` command call in `click.echo`, and `coinflip.py` imports it (`from .uwuify import uwuify`) to uwuify its own messages. Cute flip output is now `f"{side}{message}"` where `COINS_MESSAGES` fragments carry their own punctuation (no `! ` join), and a `kawa` event prints the bare uwuified message. The `mc`/`json`/`coinflip` outputs themselves still echo in place. (Authored by the user as WIP "human slop code"; the defects it shipped — nested-list `uwuify` calls, silent `secret`, ruff I001/F401 — were repaired in `151b8cc`. Don't copy the nested-list `uwuify([...])` call pattern.)

## Critical Implementation Paths

### Minecraft coordinate conversion
- Nether → Overworld: multiply by **8**; Overworld → Nether: divide by **8**.
- Output format: `Nether: (x, z)  (σ･ω･)σ  Overworld: (X, Z)` (two spaces around kaomoji).

### Level ↔ Experience (piecewise formulas)
- `level_to_experience(level)`:
  - `level ≤ 16`: `level² + 6·level`
  - `16 < level ≤ 31`: `2.5·level² − 40.5·level + 360`
  - `level > 31`: `4.5·level² − 162.5·level + 2220`
  - Easter eggs: `level == 21863` (max XP message), `level > 21863` (break-the-game message).
- `experience_to_level(xp)`:
  - `xp ≤ 352`: `√(xp + 9) − 3`
  - `352 < xp ≤ 1507`: `8.1 + √(0.4·(xp − 195.975))` i.e. `(81/10) + sqrt((2/5)*(xp − 7839/40))`
  - `xp > 1507`: `(325/18) + √((2/9)·(xp − 54215/72))`
  - Easter eggs: `xp == 2147483647`, `xp > 2147483647`.
  - Level results print with 2 decimals via `comma()`.

### Uwuify
- Words are uwuified **individually** (list of tokens), then rejoined with spaces — preserves word boundaries.
- `uwuify()` returns the result (string or JSON string); callers decide whether to `click.echo`. It must be given a **flat list of strings** — passing a nested list (e.g. `uwuify([COINS_MESSAGES])`) crashes uwuipy with `AttributeError: 'list' object has no attribute 'split'`, and because it returns **one joined string**, a whole pool must never be passed either; the correct idiom is pick-then-uwuify: `uwuify([random.choice(pool)])` (the `151b8cc` repair).

### Coinflip output
- Cute, no event: `f"{side}{message}"` — `side` is `Heads`/`Tails`, `message` is a uwuified `COINS_MESSAGES` fragment whose own punctuation provides the separator.
- Cute, `kawa` event: bare uwuified Kawa message. Cute, `secret` event: bare **raw** (non-uwuified) placeholder message — prints since `151b8cc` (was silently dropped before).

## Design Patterns

- Adapter pattern: `cli.py` commands are adapters over module functions.
- Facade: package `__init__.py` files act as facades via star-exports.
- Graceful degradation for external resources (banner, distribution metadata).
- Cross-cutting concern injection: the `output_mode` decorator applies output-formatting options uniformly (decorator pattern + context propagation via `ctx.obj`).
