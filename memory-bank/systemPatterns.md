# System Patterns

## Architecture Overview

Small layered Click CLI with a strict split between command wiring, feature logic, and formatting:

```text
src/kawa/
├── __init__.py          # __version__ = "0.2.0"
├── __main__.py          # python -m kawa → cli()
├── cli.py               # Click command tree (thin; delegates to modules)
├── modules/             # Feature logic, prints via click.echo
│   ├── __init__.py      # from .minecraft import *; from .uwuify import *; from .coinflip import *; from .json_tools import *
│   ├── minecraft.py     # coordinate + XP/level math
│   ├── uwuify.py        # uwuipy wrapper
│   ├── coinflip.py      # biased coinflip + message pools
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
- **`modules/`** own the domain math and all user-facing output. They print directly with `click.echo` — there is no return-value layer.
- **`utils/`** are pure formatting functions shared by modules.

## Key Technical Decisions

1. **Click groups over subparsers**: `cli` → `mc` → `{ntow, ownt, lvxp, xplv}`; `uwuify` sits at the root. Help text lives in docstrings.
2. **Star-import export pattern**: each package's `__init__.py` re-exports with `from .module import *`; consumers do `from .modules import *`. Convention over explicitness.
3. **Print-in-place, not return**: module functions perform their own `click.echo`. New commands should follow the same shape (logic + output in the module, wiring in `cli.py`).
4. **Defensive asset/metadata loading**: banner and version are loaded in `try/except` with graceful fallbacks (`"Oops!, seem like banner is missing..."`, `"unknown"`).
5. **Float-typed coordinate args**: Click casts `x`/`z` to `float` so `no_dot_zero()` can call `.is_integer()`. XP/level args are `int` (Python 3.12+ ints also have `.is_integer()`, relied upon by `comma()`).
6. **Global output modes via decorator** (2026-10-16): `output_mode` in `cli.py` adds `--json`/`--plain` to every group and leaf command. Resolution: leaf flag > nearest ancestor group flag > `"cute"` default (`--json` wins if both given on the same level). The mode travels via Click's parent-`ctx.obj` chain, and each wrapper's callback receives a `mode` kwarg it forwards to the module function. Modules branch `mode == "json"` / `"plain"` / else cute. `json pretty` is intentionally mode-agnostic (already JSON).

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

## Design Patterns

- Adapter pattern: `cli.py` commands are adapters over module functions.
- Facade: package `__init__.py` files act as facades via star-exports.
- Graceful degradation for external resources (banner, distribution metadata).
- Cross-cutting concern injection: the `output_mode` decorator applies output-formatting options uniformly (decorator pattern + context propagation via `ctx.obj`).
