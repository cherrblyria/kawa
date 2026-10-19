# System Patterns

## Architecture Overview

Small layered Click CLI with a strict split between command wiring, feature logic, and formatting:

```text
src/kawa/
├── __init__.py          # __version__ = "0.3.1"
├── __main__.py          # python -m kawa → cli()
├── cli.py               # Click command tree (thin; delegates to modules)
├── modules/             # Feature logic (all echo; see #3, #8)
│   ├── __init__.py      # explicit imports + __all__ (since e01def6)
│   ├── minecraft.py     # coordinate + XP/level math
│   ├── uwuify.py        # uwuipy wrapper — echoes per-invocation result
│   ├── coinflip.py      # biased coinflip + easter-egg events, own Uwuipy
│   └── json_tools.py    # JSON pretty printer (file / inline / stdin -)
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

- **`cli.py`** defines root group `cli` (banner version + completion), subgroup `mc`, top-level `uwuify`/`coinflip`, and `json` group. Thin adapters: parse args with Click types, call module functions. Every group/leaf wrapped by `output_mode` (`--json`/`--plain`).
- **`modules/`** own domain math and all output. Every module prints via `click.echo` (print-in-place), and **modules never import other modules** — coinflip uses `uwuipy` directly (`3056e31`).
- **`utils/`** are pure formatting functions shared by modules.

## Key Technical Decisions

1. **Click groups**: `cli` → `mc` → `{ntow, ownt, lvxp, xplv}`; `uwuify`/`coinflip` at root; `json` → `{pretty}`. Help text lives in docstrings.
2. **Explicit export pattern** (since `e01def6`): `modules/__init__.py` lists every name + `__all__` (`run_*` names avoid star-shadowing). `utils/__init__.py` still star-exports.
3. **Print-in-place, not return**: module functions do their own `click.echo`. (Briefly violated by `f69ecbe`; reverted `3056e31`.)
4. **Defensive asset/metadata loading**: banner/version in try/except with fallbacks.
5. **Typed args**: coords use custom `FiniteFloat` (rejects NaN/inf at parse) + `check_finite`/`check_overflow` in-module (pre-math AND post-math: finite inputs can still overflow on `x*8`, e.g. `1e308*8 -> inf`); XP/level use `click.IntRange` (level 0..1e9, xp 0..1e18, indent 0..16) with no finite/overflow checks (`int` has no NaN/inf, arbitrary precision never overflows); all `mc` leaves set `MC_CONTEXT_SETTINGS` (`ignore_unknown_options`) so negatives need no `--`.
6. **Global output modes** (`output_mode` in `cli.py`): `--json`/`--plain` on every group+leaf; leaf > group > cute; both together → `UsageError`; travels via `ctx.obj`; modules branch json/plain/cute. `json pretty` ignores mode (already JSON).
7. **Coinflip easter-egg events** (`EASTER_EGG_EVENTS`; renamed from `SPECIAL_TIERS` in `2e04c07`): ordered registry `{name, chance, messages}`, independent rolls, first hit wins (kawa 1/100 → secret 1/100K → normal flip). Effective secret chance is (1-1/100)×1/100K. Rules: **(a)** cute-only (`pick_event` returns None off-cute, zero event rolls in machine modes); **(b)** `rng` injection (`pick_event(mode, rng)` / `run_coinflip(hour, mode, rng)`). `secret` messages stay placeholders. Cached `Uwuipy` via `functools.cache get_uwu()` per module.
8. **Modules never import modules** (`3056e31`): shared third-party libs get imported per-module instead.
9. **JSON hardening** (`9ef1b2d`): stdin `-`, broken-symlink/dir errors, `utf-8-sig` reads, duplicate-key stderr warnings, `NaN/Infinity` rejected, `looks_like_path` decides File-not-found vs Invalid-JSON.
10. **Exact XP math** (`6611d10` + PR #1): `xp_for_level` uses integer `//2` formulas; `experience_to_level` snaps exact hits via `round`+`xp_for_level` check; negatives rejected.

## Critical Implementation Paths

### Minecraft coordinate conversion

- Nether → Overworld ×**8**; Overworld → Nether ÷**8**.
- Cute format (since `a8f696f`): `(x: .. y: ..) in Nether is (x: .. y: ..) in Overworld  /ᐠ｡ꞈ｡ᐟ\` with random `BORDER_MESSAGE` appended; XP/level lines use `/ᐠ｡‸｡ᐟ\`.
- World border: `|x|>30M or |z|>30M` appends border message (cute only).

### Level ↔ Experience (piecewise)

- `level_to_experience`: `≤16`: `l²+6l`; `≤31`: `(5l²-81l+720)//2`; else `(9l²-325l+4440)//2`. Eggs: `==21863` max-XP msg, `>21863` break msg.
- `experience_to_level`: `≤352`: `√(xp+9)-3`; `≤1507`: `8.1+√(0.4·(xp-195.975))`; else `(325/18)+√((2/9)·(xp-54215/72))`; exact-hit snap; 2-decimal via `comma()`. Eggs at `==2147483647` / above.

### Uwuify

- Words uwuified **individually**, rejoined with spaces. Echoes result (cute: string; json: `{"result": …}`). Needs flat list — nested lists crash uwuipy. Coinflip does **not** use it.

### Coinflip output

- Cute, no event: `f"{side}{message}"` (fragment punctuation is the separator). Cute kawa: bare uwuified message. Cute secret: bare raw placeholder. `--json`: `{"result": side.lower(), "message": raw-fragment}`. `--plain`: `side.lower()` only.

## Design Patterns

- Adapter: `cli.py` over module functions. Facade: package `__init__` files. Graceful degradation for banner/metadata. Cross-cutting decorator (`output_mode` + `ctx.obj` propagation).
