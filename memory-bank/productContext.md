# Product Context

## Why Kawa Exists

Kawa is a hobby/joy project: a bundle of tiny CLI utilities that are useful in passing (mostly Minecraft math) and delightful to use. It exists to:

- Save Minecraft players from mental math when linking Nether/Overworld portals or planning XP grinds.
- Provide a fun `uwuify` text command in the same binary.
- Pretty-print JSON from files, inline strings, or stdin pipes.
- Act as a personal, well-packaged CLI project that ships everywhere (PyPI-style installs, Nix, standalone binaries).

## How It Should Work

- Run `kawa --help` (or `kawa -h`) to discover grouped commands. Every command has a descriptive canonical name plus short/legacy aliases (`kawa minecraft`/`kawa mc`, `ntow`/`nt`, `ownt`/`ow`, `lvxp`/`lv`, `xplv`, `uwu`, `cf`), so old and short spellings both work.
- Every command accepts **`--plain`** (undecorated result only, e.g. `heads`, `5816, 727`) and **`--json`** (single-line JSON) output modes, usable anywhere on the command line; mode resolves as leaf flag > group flag > cute default. The two flags together raise `UsageError`. `json pretty` accepts the flags but ignores them (already JSON).
- Negative coordinates work directly with no `--` separator (`MC_CONTEXT_SETTINGS` sets `ignore_unknown_options` on all `minecraft` leaf commands (alias `mc`)).
- Numbers are formatted prettily: integers with thousands separators and no `.0`; floats shown with 2 decimals (`comma`, `no_dot_zero` helpers).
- `kawa --version` prints the ASCII banner (loaded from `src/kawa/assets/banner.txt`) plus the version.
- Boundary values get playful easter-egg messages (max XP level 21863, `2147483647` XP; world-border coordinates pick randomly from a 4-line `BORDER_MESSAGE` list).
- **Coinflip text is uwuified**: the flip prints `Heads`/`Tails` plus a random uwuified fragment from `COINS_MESSAGES` (e.g. `"! That's it"` — the fragment carries the punctuation), uwuified in-place via coinflip's own cached `get_uwu()` `Uwuipy` instance (independent of the `uwuify` command).
- **Special events are cute-mode-only easter eggs**: a `kawa` roll (**1/100**) replaces the coin result with a uwuified Kawa message; `--json`/`--plain` are machine output, never roll events, and must stay deterministic heads/tails. A further `secret` event (1/100K) is a placeholder for a planned interactive lore event. `--json` coinflip now also ships a raw (non-uwuified) `message` field.
- Shell completion is available via the option injected by `auto-click-auto`.
- README carries a vibe-coded warning banner ("USE THIS AS YOUR OWN RISK AND MENTAL, I vibe coded this FOR FUN").

## UX Goals

- **Cute over corporate**: kaomoji, banner, casual wording — friendly and sometimes playful.
- **Zero-config**: no config files, no flags needed for core commands — plain positional arguments.
- **Fast feedback**: commands are pure math/string work; instant output.
- **Forgiving**: banner/version loading wrapped in try/except so a missing asset degrades gracefully instead of crashing.

## Users

- Primarily the author; open to anyone who finds it cute/useful on GitHub.
