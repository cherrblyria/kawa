# Tech Context

## Stack

| Area | Technology |
|---|---|
| Language | Python **≥ 3.14** (pinned `3.14` in `.python-version`; flake uses `pkgs.python314`) |
| CLI framework | **Click ≥ 8.1.8** |
| Shell completion | **auto-click-auto ≥ 0.1.6** (`enable_click_shell_completion_option`) |
| Uwuify engine | **uwuipy ≥ 0.1.5** |
| Build backend | **hatchling** (wheel packages `src/kawa`) |
| Package/venv manager | **uv** (`uv sync --dev`, `uv run ...`) |
| Linter/formatter | **ruff ≥ 0.6** (`[tool.ruff] src = ["src"]`) — no config beyond that |
| Binary packaging | **PyInstaller ≥ 6.10** via `kawa.spec` |
| Nix packaging | flake with **uv2nix + pyproject-nix + pyproject-build-systems**, `sourcePreference = "wheel"` |
| CI/CD | GitHub Actions (`.github/workflows/ci.yml`, `release.yml`) |
| Tests | **None (pytest not present)** — only smoke commands in CI |

## Development Setup

```bash
git clone https://github.com/cherrblyria/kawa
cd kawa
uv sync --dev            # creates .venv with runtime + dev deps

# run
uv run kawa --help
uv run kawa mc ntow 727 90.875
uv run kawa uwuify The quick brown fox jumps over the lazy dog
python -m kawa --help    # also works via __main__.py

# lint / format
uv run ruff check .
uv run ruff format .

# build standalone binary
uv run pyinstaller kawa.spec
./dist/kawa --version
```

Nix: `nix run github:cherrblyria/kawa` (or consume `inputs.kawa.packages.${pkgs.system}.default`).

## Entry Points

- Console script: `kawa = "kawa.cli:cli"` (`[project.scripts]` in `pyproject.toml`).
- Module execution: `python -m kawa` → `src/kawa/__main__.py`.
- PyInstaller entry: `src/kawa/__main__.py`, bundles `src/kawa/assets` as `kawa/assets`, UPX enabled, console app named `kawa`.

## Packaging & Distribution Matrix

- **pip/pipx/uv**: `pipx install git+https://github.com/cherrblyria/kawa`
- **Nix flake**: outputs `packages` + `apps` for `x86_64-linux`, `aarch64-linux`, `x86_64-darwin`, `aarch64-darwin`.
- **Release binaries**: triggered by pushing tag `v*.*.*`; matrix builds:
  - `kawa-linux-x86_64` (ubuntu-latest)
  - `kawa-windows-x86_64.exe` (windows-latest)
  - `kawa-macos-x86_64` (macos-15-intel)
  - `kawa-macos-arm64` (macos-15)
  - then creates a GitHub Release with all artifacts (`softprops/action-gh-release@v2`).

## CI Behavior (important nuances)

- `ci.yml` runs on **all branch pushes** and PRs (tags `v*.*.*` excluded).
- Lint (`ruff check`) and format check (`ruff format --check`) are **`continue-on-error: true`** — they report but do **not** fail the build today.
- Smoke tests (blocking): `kawa mc ntow 10 20`, `kawa mc ownt 80 160`, `kawa uwuify ...`.
- Second job `build-check` builds the PyInstaller binary and sanity-runs `./dist/kawa mc ntow 10 20`.

## Technical Constraints

- Python 3.14-only floor: cannot rely on older interpreters; conversely avoid ≥3.15-only APIs.
- Star-imports mean module `__init__` files control the public surface — add new helpers there or they won't be visible to `from ..utils import *`.
- `no_dot_zero()`/`comma()` call `.is_integer()` — inputs must be `int`/`float` (never `str`).
- Banner must remain in `kawa.spec` `datas` or `--version` degrades to the fallback message.
- Version appears in both `pyproject.toml` and `src/kawa/__init__.py` — bump both on release.
- `.gitignore` ignores `.vscode/*` except `extensions.json`; `memory-bank/` and `.clinerules/` are not yet ignored or committed.

## Tool Usage Patterns

- uv is the single source of truth for deps (`uv.lock` committed).
- ruff is invoked only through `uv run`.
- GitHub Actions installs Python via `uv python install 3.14` (no `actions/setup-python`).
