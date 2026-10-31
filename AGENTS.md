# AGENTS.md

## Project

`kawa` — a small joke CLI (Minecraft calculators, uwuify, coinflip, JSON pretty-print). Click-based, Python 3.14, packaged with hatchling, distributed as wheel + PyInstaller binary + Nix flake.

## Commands

```bash
uv sync --dev                                # setup (Python 3.14 via .python-version)
uv run ruff check .                          # lint
uv run ruff format --check .                 # format check (CI fails if unformatted)
uv run python -m unittest discover -s tests -v   # all tests (stdlib unittest, NOT pytest)
uv run kawa <args>                           # run CLI in-place
uv run pyinstaller kawa.spec                 # build standalone binary -> dist/kawa
```

CI order (`.github/workflows/ci.yml`): lint → format check → unittest → smoke-run CLI commands → PyInstaller build + run `dist/kawa`.

Single test:
```bash
uv run python -m unittest tests.test_minecraft_cli.MinecraftCliTests.test_nether_to_overworld_json -v
uv run python -m unittest tests.test_json_cli -v   # whole file
```

## Architecture

- `src/kawa/cli.py` — single Click app (`cli` entrypoint, `python -m kawa` via `__main__.py`). All commands defined here.
- `src/kawa/modules/` — feature logic; each function takes `mode` ("cute" | "json" | "plain") and prints via `click.echo` (does not return values).
- `src/kawa/utils/format.py` — number formatting helpers (`no_dot_zero`, `comma`).
- `src/kawa/assets/banner.txt` — bundled resource; loaded via `importlib.resources.files("kawa")` with graceful fallback. New assets must be added to `kawa.spec` `datas` or PyInstaller builds will miss them.

## Conventions

- **Output modes**: every command is wrapped with the `output_mode` decorator (`cli.py`). `--json` and `--plain` are mutually exclusive; mode resolves leaf flag → group flag → cute default. New commands must use `@output_mode` and accept a `mode` param; JSON output must use `allow_nan=False` (tests assert no `NaN`/`Infinity` in JSON).
- **Aliases**: commands use `click_aliases.ClickAliasedGroup` (e.g. `mc` = `minecraft`, `ntow` = `nether`). Add aliases via the `aliases=[...]` kwarg.
- **Tests assert exact cute output strings** (kaomoji suffixes like `/ᐠ｡ꞈ｡ᐟ\`). Changing user-facing text requires updating both tests and README examples — `tests/test_minecraft_cli.py::test_readme_examples` pins README output verbatim.
- **Version is defined twice**: `pyproject.toml` (authoritative; CLI reads it via `importlib.metadata`) and `src/kawa/__init__.py::__version__`. Keep both in sync when releasing.
- **Negative-number args**: `minecraft` commands use `ignore_unknown_options=True` + a custom `FiniteFloat` param type so `kawa mc ntow -5 -3` works without `--`. Don't "fix" this by removing those settings.
- **Windows encoding**: `cli.py` reconfigures stdout/stderr to UTF-8 with `errors="replace"`. `tests/test_encoding.py` spawns a subprocess with `PYTHONIOENCODING=cp1252` + `PYTHONPATH=src` to guard this — don't remove the reconfigure block.
- **Ruff**: minimal config (`src = ["src"]` in `pyproject.toml`); default line length (88). No typechecker (no mypy/pyright) and no pre-commit hooks in CI.
- **No pytest**: `dependency-groups.dev` only has pyinstaller + ruff. Tests are stdlib `unittest` with `click.testing.CliRunner`.
- **Commit messages**: follow Conventional Commits (`feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `perf:`), lowercase imperative summary (e.g. `feat: add uuid command`). Only commit when explicitly asked.

## Releases

Pushing a `v*.*.*` tag triggers `.github/workflows/release.yml`: PyInstaller builds on Linux/Windows/macOS (x86_64 + arm64), uploaded to a GitHub Release. Bump the version in both `pyproject.toml` and `src/kawa/__init__.py` before tagging.

## Nix

`flake.nix` (uv2nix + pyproject-nix, Python 3.14) exposes `packages.default` and `apps.default`; `nix run` works locally but Nix is not exercised in CI.
