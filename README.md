<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Cascadia+Code&size=22&pause=1000&color=FED0FF&random=true&width=435&lines=awaK;Kaw;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa+%3C3;Kawa+~;Kawa+~;Kawaii+%2F%2F%2F;Kawaii+~;MudaKawa" alt="Typing SVG" /></a>

> "A set of useless cute little CLI tools for... whatever."

> [!WARNING]
> USE THIS AS YOUR OWN RISK AND MENTAL, I vibe coded this FOR FUN not for real usage.

##### on this page

- [Features](#features)
  - [Minecraft](#minecraft)
  - [Uwuify](#uwuify)
  - [Coinflip](#coinflip)
  - [UUID](#uuid)
  - [JSON](#json)
- [Installation](#installation)
  - [Nix / NixOS (Flake)](#nix--nixos-flake)
  - [pip / pipx](#pip--pipx)
  - [Prebuilt binaries](#prebuilt-binaries)
  - [From source](#from-source)
- [License](#license)

### Features

#### Minecraft

Minecraft calculators for coordinates and XP, plus a storage converter. All
commands work in cute, plain, and JSON output modes.

##### Stack / Shulker box converter

Convert items, stacks, and shulker boxes. Pick the input command: `item`,
`stack`, or `shulker` (alias `sb`), then choose `to-item`, `to-stack`, or
`to-shulker` (alias `to-sb`).

- `-s, --stack` sets how many items make a stack (default `64`).
- `-l, --large-chest` uses 54-slot containers instead of the default
  27-slot shulker boxes.
- Results that do not divide evenly include a breakdown of full containers,
  full stacks, and leftover items.

```bash
$ kawa mc item 128 to-stack
that's 2 stack(s) of item(s) /ᐠ_ ꞈ _ᐟ\ɴʏᴀ~
```

```
$ kawa mc item 1800 to-shulker
that's 1 shulker box(es), 1 stack(s) and 8 item(s) /ᐠ_ ꞈ _ᐟ\ɴʏᴀ~
```

```
$ kawa mc stack 9 to-item -s 16
that's 144 item(s) /ᐠ_ ꞈ _ᐟ\ɴʏᴀ~
```

```bash
$ kawa mc item 100 to-stack
that's 1 stack(s) and 36 item(s) /ᐠ_ ꞈ _ᐟ\ɴʏᴀ~
```

##### Nether ↔ Overworld coordinates calculator

Convert between Nether and Overworld coordinates using the vanilla 1:8 ratio.
`ntow`/`nt` goes Nether → Overworld, while `ownt`/`ow` goes the other way.
Decimal and negative coordinates are supported.

```bash
$ kawa mc ntow 727 -90.875
(x: 727 y: -90.875) in Nether is (x: 5816 y: -727) in Overworld  /ᐠ｡ꞈ｡ᐟ\
```

```bash
$ kawa mc ownt 727 5816
(x: 727 y: 5816) in Overworld is (x: 90.875 y: 727) in Nether  /ᐠ｡ꞈ｡ᐟ\
```

Plain mode prints `x, z`; JSON mode prints `{"x": ..., "z": ...}`. Cute mode
adds a world-border quip for coordinates past ±30,000,000.

##### Level ↔ Experience calculator

Convert levels to total experience with `lvxp`/`lv`, or experience back into a
level with `xplv`/`xp`. Both directions use the vanilla XP formulas. Reverse
conversion stays fractional when the XP amount does not land exactly on a
level.

```bash
$ kawa mc lvxp 21864
Level 21,864 is 2,147,604,552 Experience /ᐠ｡‸｡ᐟ\
 - I think this amount of XP can break the game :3
```

```bash
$ kawa mc xplv 2147483647
2,147,483,647 Experience is Level 21,863.39 /ᐠ｡‸｡ᐟ\
 - Have you ever reach this level before?
```

#### Uwuify

Powered by [uwuipy](https://github.com/Cuprum77/uwuipy). Pass one or more words
as arguments; multiple arguments are joined with spaces. Quote text that
contains shell-sensitive characters.

```bash
$ kawa uwuify The quick brown fox jumps over the lazy dog
The q-q-quick bwown fox jyumps uvw the wazy dog
```

`--json` wraps the text as `{"result": "..."}`.

#### Coinflip

Flip a coin. Cute mode may add a random message (and very rarely an easter egg);
plain mode prints only `heads` or `tails`, while JSON mode returns
`{"result": ..., "message": ...}`.

```bash
$ kawa coinflip
Heads! As I expected..
```

#### UUID

Generate a random UUID. Defaults to version 4; pass `--v7` for a time-ordered
version 7 UUID.

```bash
$ kawa uuid
63a5860d-22c0-45ab-92be-c9f2a158baef /ᐠ‸⑅‸ ᐟ\ﾉ
```

```bash
$ kawa uuid --v7
0199e1a0-1a2b-7c3d-8e4f-5a6b7c8d9e0f /ᐠ‸⑅‸ ᐟ\ﾉ
```

Use `--plain` for just the UUID, or `--json` for the UUID and its version:

```bash
$ kawa uuid --plain
63a5860d-22c0-45ab-92be-c9f2a158baef
```

```bash
$ kawa uuid --v7 --json
{"uuid": "0199e1a0-1a2b-7c3d-8e4f-5a6b7c8d9e0f", "version": 7}
```

#### JSON

Pretty-print JSON from a file path, a raw JSON string, or stdin. Use `-i` /
`--indent` to set indentation (`0`–`16`, default `4`) and `-s` / `--sort-keys`
to sort object keys alphabetically.

Duplicate keys print a warning to stderr and the last value wins. Non-standard
values such as `NaN` and `Infinity` are rejected, and UTF-8 BOM files are
supported.

```bash
$ kawa json pretty data.json
{
    "name": "kawa",
    "kawaii": true
}
```

```bash
$ kawa json pretty '{"b": 1, "a": 2}' --sort-keys
{
    "a": 2,
    "b": 1
}
```

Read from stdin with `-`:

```bash
$ echo '{"a": 1}' | kawa json pretty -
{
    "a": 1
}
```

#### Output modes

Every command accepts `--json` or `--plain` (undecorated result). The two flags
are mutually exclusive. Flags can be passed to a command or to its group, so
`kawa --json mc ntow 10 20` and `kawa mc ntow 10 20 --json` behave the same.

```bash
$ kawa mc ntow 10 20 --json
{"x": 80, "z": 160}
```

```bash
$ kawa mc ntow 10 20 --plain
80, 160
```

```
$ kawa coinflip --plain
heads
```

JSON output is always strict (`NaN` and `Infinity` are never emitted).

Shell completion is available via `--autocomplete`.

### Installation

#### Nix / NixOS (Flake)

Since this project is a flake, you can just run it like this:

```bash
nix run github:cherrblyria/kawa
```

Or install it on your system just like any other flake:

```nix
# flake.nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    kawa.url = "github:cherrblyria/kawa";
  };
}
```

```nix
# configuration.nix
{ pkgs, inputs, ... }: {
  environment.systemPackages = [
    inputs.kawa.packages.${pkgs.system}.default
  ];
}
```

#### pip / pipx

```bash
pipx install git+https://github.com/cherrblyria/kawa
```

or with `uv`:

```bash
uv tool install git+https://github.com/cherrblyria/kawa
```

#### Prebuilt binaries

Grab a standalone binary from the [Releases page](https://github.com/cherrblyria/kawa/releases/latest)

#### From source

```bash
git clone https://github.com/cherrblyria/kawa
cd kawa
uv sync --dev
uv run pyinstaller kawa.spec
./dist/kawa --version
```

### License

MIT — see [LICENSE](./LICENSE)
