## Kawa

> "A set of useless cute little CLI tools for Minecraft and.. ahh... that's it (for now)"

### Installation

#### Nix/NixOS (Flake)

since this project is flake you can just run it like this.

```bash
nix run github:cherrblyria/kawa
```

or install it on your system just like other flake

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
uv run kawa mc ntow 10 20
```

### Example

here're some example usages

```bash
$ kawa mc ntow 10 20
Nether: (10, 20)  (σ･ω･)σ  Overworld: (80, 160)

$ kawa mc ownt 80 160
Overworld: (80, 160)  (σ･ω･)σ  Nether: (10, 20)
```

### License

MIT — see [LICENSE](./LICENSE)
