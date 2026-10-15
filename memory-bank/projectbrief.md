# Project Brief

## Overview

**Kawa** (`kawa`) — "A set of useless cute little CLI tools for Minecraft and.. ahh... that's it (for now)".

A small, playful Python CLI tool collection. Current scope:

1. **Minecraft tools** (`kawa mc ...`)
   - Nether ↔ Overworld coordinate calculator (`ntow`, `ownt`)
   - Level ↔ Experience calculator (`lvxp`, `xplv`)
2. **Uwuify** (`kawa uwuify ...`) — text transformation powered by [uwuipy](https://github.com/Cuprum77/uwuipy)
3. **JSON pretty printer** (`kawa json pretty ...`) — file path or raw string input, stdlib `json`
4. **Coinflip** (`kawa coinflip`) — biased coinflip with swappable message pools (AM/PM bias)

## Core Requirements & Goals

- Ship as a single `kawa` command with cute kaomoji-flavored output (e.g. `(σ･ω･)σ`, `(σ≧∀≦)σ`) and an ASCII banner in `--version`.
- Distribute through as many channels as possible:
  - **Nix flake** (`nix run github:cherrblyria/kawa`) via uv2nix
  - **pip / pipx / uv tool** from the git repo
  - **Standalone binaries** (PyInstaller) attached to GitHub Releases
  - **From source** with `uv sync --dev`
- Keep the codebase tiny, dependency-light, and readable.
- Support shell completion out of the box.

## Project Identity

- Repository: https://github.com/cherrblyria/kawa
- License: MIT
- Author: cherrblyria
- Current version: **0.2.0** (tags: `v0.1.0`, `v0.2.0`)
- Branch: `main`

## Scope Boundaries

- No web UI, no server, no persistence — pure CLI.
- "Useless cute" is the brand: features are intentionally small and fun; the README explicitly implies more tools may come later ("...that's it (for now)").
