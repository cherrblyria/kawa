# Project Brief

## Overview

**Kawa** (`kawa`) — "A set of useless cute little CLI tools for... whatever." (README tagline since `acc29c9`).

A small, playful Python CLI tool collection. Current scope:

1. **Minecraft tools** (`kawa mc ...`)
   - Nether ↔ Overworld coordinate calculator (`ntow`, `ownt`)
   - Level ↔ Experience calculator (`lvxp`, `xplv`)
2. **Uwuify** (`kawa uwuify ...`) — text transformation powered by [uwuipy](https://github.com/Cuprum77/uwuipy)
3. **Coinflip** (`kawa coinflip`) — biased coinflip (AM/PM) with short uwuified message fragments (`COINS_MESSAGES`) + cute-mode-only easter-egg events: kawa 1/100, secret 1/100K placeholder (pending lore)
4. **JSON pretty printer** (`kawa json pretty ...`) — file path, raw string, or stdin (`-`) input, stdlib `json`

## Core Requirements & Goals

- Ship as a single `kawa` command with cute kaomoji-flavored output and an ASCII banner in `--version`.
- Distribute through as many channels as possible:
  - **Nix flake** (`nix run github:cherrblyria/kawa`) via uv2nix
  - **pip / pipx / uv tool** from the git repo
  - **Standalone binaries** (PyInstaller) attached to GitHub Releases
  - **From source** with `uv sync --dev`
- Keep the codebase tiny, dependency-light, and readable.
- Support shell completion out of the box.
- Real `unittest` suite (`tests/`, 58 tests on main; tree tests green, README still old format) + blocking ruff + smoke tests in CI.

## Project Identity

- Repository: https://github.com/cherrblyria/kawa
- License: MIT
- Author: cherrblyria
- Current version: **0.3.1 in code** (`pyproject.toml`, `src/kawa/__init__.py`, `uv.lock` — bumped `9083713` + `2dd4856`/`d758923`, merged as `0a10611`). Tags: `v0.1.0`, `v0.2.0`, `v0.3.0`, `v0.3.1` (on `62a34a2`), `v0.3.2` (on `b9fe2ac`) — **both tags predate HEAD, so code (0.3.1) disagrees with latest tag (v0.3.2): version/tag mismatch, see activeContext.md**.
- Branch: `main` (HEAD `0a10611`, in sync with `origin/main`; `fix/edge-cases` merged via PR #4)

## Scope Boundaries

- No web UI, no server, no persistence — pure CLI.
- "Useless cute" is the brand: features are intentionally small and fun; the open-ended README tagline ("...for... whatever.") implies more tools may come later.
