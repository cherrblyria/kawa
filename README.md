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

##### Stack / Shulker box converter

Convert items, stacks, and shulker boxes with an optional custom stack size.

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

##### Nether ↔ Overworld coordinates calculator

```bash
$ kawa mc ntow 727 -90.875
(x: 727 y: -90.875) in Nether is (x: 5816 y: -727) in Overworld  /ᐠ｡ꞈ｡ᐟ\
```

```bash
$ kawa mc ownt 727 5816
(x: 727 y: 5816) in Overworld is (x: 90.875 y: 727) in Nether  /ᐠ｡ꞈ｡ᐟ\
```

##### Level ↔ Experience calculator

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

powered by [uwuipy](https://github.com/Cuprum77/uwuipy)

```bash
$ kawa uwuify The quick brown fox jumps over the lazy dog
The q-q-quick bwown fox jyumps uvw the wazy dog
```

#### Coinflip

Flip a coin

```bash
$ kawa coinflip
Heads! As I expected..
```

#### UUID

Generate a random UUID. Defaults to version 4; use `--v7` for a time-ordered
version 7 UUID.

```bash
$ kawa uuid
63a5860d-22c0-45ab-92be-c9f2a158baef /ᐠ‸⑅‸ ᐟ\ﾉ
```

```bash
$ kawa uuid --v7 --plain
0199e1a0-1a2b-7c3d-8e4f-5a6b7c8d9e0f
```

#### JSON

Pretty-print JSON from a file path or a raw string.

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

Every command accepts `--json` or `--plain`
(undecorated result). The two flags are mutually exclusive.

```bash
$ kawa mc ntow 10 20 --json
{"x": 80, "z": 160}
```

```
$ kawa coinflip --plain
heads
```

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
