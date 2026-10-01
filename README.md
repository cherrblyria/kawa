<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Cascadia+Code&size=22&pause=1000&color=FED0FF&random=true&width=435&lines=Kawa;Kawa+~;Kawa;Kawa+%3C3;Kawaii+~;Kawaii+%2F%2F%2F;Kawa;Kawa;Kawa;Kawa+~;MudaKawa;Kawa;awaK;Kawa;Kawa;Kaw;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa;Kawa" alt="Typing SVG" /></a>

> "A set of useless cute little CLI tools for Minecraft and.. ahh... that's it (for now)"

##### on this page

- [Features](#features)
  - [Minecraft](#minecraft)
  - [Uwuify](#uwuify)
- [Installation](#installation)
  - [Nix / NixOS (Flake)](#nix--nixos-flake)
  - [pip / pipx](#pip--pipx)
  - [Prebuilt binaries](#prebuilt-binaries)
  - [From source](#from-source)
- [License](#license)

### Features

#### Minecraft

##### Nether ↔ Overworld coordinates calculator

```bash
$ kawa mc ntow 727 90.875
Nether: (727, 90.875)  (σ･ω･)σ  Overworld: (5816, 727)
```

```bash
$ kawa mc ownt 727 5816
Overworld: (727, 5816)  (σ･ω･)σ  Nether: (90.875, 727)
```

##### Level ↔ Expreience calculator

```bash
$ kawa mc lvxp 21864
Level: 21,864  (σ≧∀≦)σ  Expreience: 2,147,604,552
```

```bash
$ kawa mc xplv 2147483647
Expreience: 2,147,483,647  (σ≧∀≦)σ  Level: 21,863.39
```

#### Uwuify

powered by [uwuipy](https://github.com/Cuprum77/uwuipy)

```bash
$ kawa uwuify The quick brown fox jumps over the lazy dog
The q-q-quick bwown fox jyumps uvw the wazy dog
```

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
