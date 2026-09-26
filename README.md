## Kawa

> "A set of useless cute little CLI tools for Minecraft and.. ahh... that's it (for now)"

##### on this page

- [Installation](#installation)
  - [Nix / NixOS (Flake)](#nix--nixos-flake)
  - [pip / pipx](#pip--pipx)
  - [Prebuilt binaries (Soon)](#prebuilt-binaries)
  - [From source](#from-source)
- [Shell Completion](#shell-completion)
- [Usage](#usage)
- [License](#license)

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

Grab a standalone binary from the [~~Releases page~~](https://github.com/cherrblyria/kawa/releases/latest) — nope, there's no release right now.

#### From source

```bash
git clone https://github.com/cherrblyria/kawa
cd kawa
uv sync --dev
uv run kawa mc ntow 10 20
```

### Shell Completion

Kawa supports tab-completion for `bash`, `zsh`, and `fish` via [`argcomplete`](https://github.com/kislyuk/argcomplete). Pick your shell below and add the snippet to your config.

| Shell | Setup                                                                                                         |
| ----- | ------------------------------------------------------------------------------------------------------------- |
| bash  | Add to `~/.bashrc`: `eval "$(register-python-argcomplete kawa)"`                                              |
| zsh   | Add to `~/.zshrc`: `autoload -U bashcompinit; bashcompinit` then `eval "$(register-python-argcomplete kawa)"` |
| fish  | Run once: `register-python-argcomplete --shell fish kawa > ~/.config/fish/completions/kawa.fish`              |

After that, restart your shell (or `source` the config)

### Usage

Here're some example usages:

```bash
$ kawa mc ntow 10 20
Nether: (10, 20)  (σ･ω･)σ  Overworld: (80, 160)

$ kawa mc ownt 80 160
Overworld: (80, 160)  (σ･ω･)σ  Nether: (10, 20)

$ kawa uwuify "hello world"
hewwo wowwd
```

### License

MIT — see [LICENSE](./LICENSE)
