# Product Context

## Why Kawa Exists

Kawa is a hobby/joy project: a bundle of tiny CLI utilities that are useful in passing (mostly Minecraft math) and delightful to use. It exists to:

- Save Minecraft players from mental math when linking Nether/Overworld portals or planning XP grinds.
- Provide a fun `uwuify` text command in the same binary.
- Act as a personal, well-packaged CLI project that ships everywhere (PyPI-style installs, Nix, standalone binaries).

## How It Should Work

- Run `kawa --help` (or `kawa -h`) to discover grouped commands.
- Every command prints a single human-readable line with a kaomoji separator between input and result, e.g.:

  ```text
  $ kawa mc ntow 727 90.875
  Nether: (727, 90.875)  (σ･ω･)σ  Overworld: (5816, 727)
  ```

- Numbers are formatted prettily: integers with thousands separators and no `.0`; floats shown with 2 decimals (`comma`, `no_dot_zero` helpers).
- `kawa --version` prints the ASCII banner (loaded from `src/kawa/assets/banner.txt`) plus the version.
- Boundary values get playful easter-egg messages (max XP level 21863, `2147483647` XP, etc.).
- Shell completion is available via the option injected by `auto-click-auto`.

## UX Goals

- **Cute over corporate**: kaomoji, banner, casual wording (even typos like "Expreience" are part of the current voice — see `progress.md` quirks).
- **Zero-config**: no config files, no flags needed for core commands — plain positional arguments.
- **Fast feedback**: commands are pure math/string work; instant output.
- **Forgiving**: banner/version loading wrapped in try/except so a missing asset degrades gracefully instead of crashing.

## Users

- Primarily the author; open to anyone who finds it cute/useful on GitHub.
