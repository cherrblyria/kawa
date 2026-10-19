# Tech Context

## Stack

| Area | Technology |
|---|---|
| Language | Python **≥ 3.14** (`.python-version` = `3.14`; flake `pkgs.python314`) |
| CLI framework | **Click ≥ 8.1.8** |
| Shell completion | **auto-click-auto ≥ 0.1.6** |
| Uwuify engine | **uwuipy ≥ 1.0.0** (bumped from 0.1.5 on main) |
| Build backend | **hatchling** (wheel packages `src/kawa`) |
| Package/venv manager | **uv** (`uv sync --dev`, `uv run ...`) |
| Linter/formatter | **ruff ≥ 0.6** (`[tool.ruff] src = ["src"]`) — **blocking in CI** (PR #2) |
| Binary packaging | **PyInstaller ≥ 6.10** via `kawa.spec` |
| Nix packaging | flake with **uv2nix + pyproject-nix + pyproject-build-systems**, `sourcePreference = "wheel"` |
| CI/CD | GitHub Actions (`ci.yml`, `release.yml`) |
| Tests | **`unittest` stdlib, 58 tests** in `tests/` (`test_minecraft_cli` 26, `test_json_cli` 17, `test_coinflip` 8, `test_uwuify` 5, `test_encoding` 2) — no pytest |

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

# lint / format / tests
uv run ruff check .
uv run ruff format --check .
uv run python -m unittest discover -s tests -v

# build standalone binary
uv run pyinstaller kawa.spec
./dist/kawa --version
```

Nix: `nix run github:cherrblyria/kawa` (or consume `inputs.kawa.packages.${pkgs.system}.default`).

## Entry Points

- Console script: `kawa = "kawa.cli:cli"` (`[project.scripts]`).
- Module execution: `python -m kawa` → `src/kawa/__main__.py`.
- PyInstaller entry: `src/kawa/__main__.py`, bundles `src/kawa/assets` as `kawa/assets`, UPX enabled, console app named `kawa`.

## Packaging & Distribution Matrix

- **pip/pipx/uv**: `pipx install git+https://github.com/cherrblyria/kawa`
- **Nix flake**: outputs `packages` + `apps` for `x86_64-linux`, `aarch64-linux`, `x86_64-darwin`, `aarch64-darwin`.
- **Release binaries**: tag `v*.*.*` → matrix (`kawa-linux-x86_64`, `kawa-windows-x86_64.exe`, `kawa-macos-x86_64`, `kawa-macos-arm64`) → GitHub Release with generated notes.

## CI Behavior

- `ci.yml` runs on **all branch pushes** + PRs (tags `v*.*.*` excluded). Jobs: `check` (ubuntu), `windows-check`, `build-check` (needs `check`).
- **Ruff lint + format-check are blocking** (PR #2 removed `continue-on-error`).
- **Unit tests are blocking**: `uv run python -m unittest discover -s tests -v` on both ubuntu + windows.
- Smoke tests (blocking): `mc ntow/ownt`, negative coords, `uwuify`, `coinflip` (cute + `--plain`), `json pretty -` via stdin pipe; windows job has a piped smoke test; `build-check` builds the binary and sanity-runs it.

## Technical Constraints

- Python 3.14-only floor; avoid ≥3.15-only APIs.
- `modules/__init__.py` is explicit (`__all__`) — new helpers must be added there to be exported; `utils/__init__.py` still star-exports.
- `no_dot_zero()`/`comma()` call `.is_integer()` — inputs must be `int`/`float` (never `str`); coords additionally pass through `FiniteFloat`.
- Banner must remain in `kawa.spec` `datas` or `--version` degrades to fallback.
- Version in both `pyproject.toml` and `src/kawa/__init__.py` — bump both (currently 0.3.1, matching latest tag `v0.3.1`).
- `.gitignore` ignores `.vscode/*` except `extensions.json`; `memory-bank/` and `.clinerules/` are committed, not ignored.

## Tool Usage Patterns

- uv is the single source of truth (`uv.lock` committed).
- ruff + tests invoked only through `uv run`.
- GitHub Actions installs Python via `uv python install 3.14`.
