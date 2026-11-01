# Kawa Architecture

This document separates the current implementation from the intended direction. The current code is authoritative; target architecture ideas are guidance for future work, not a description of existing modules.

## Current implementation

Kawa is a Python command-line application.

### Main technologies

- Python 3.14.
- Click for the CLI.
- click-aliases for command aliases.
- hatchling for packaging.
- Ruff for linting and formatting.
- Python standard-library unittest for tests.
- PyInstaller for standalone binaries.
- A Nix flake using uv2nix and pyproject-nix.

### Source layout

- `src/kawa/cli.py`: main Click application and command definitions.
- `src/kawa/__main__.py`: module entry point.
- `src/kawa/modules/`: feature implementations.
- `src/kawa/utils/`: shared utilities.
- `src/kawa/assets/`: bundled assets.
- `tests/`: test suite.
- `kawa.spec`: PyInstaller build configuration.
- `flake.nix`: Nix packaging and app definitions.

See [AGENTS.md](../AGENTS.md) for implementation constraints and development commands.

### Current CLI behavior

- Commands are defined in the main Click application.
- Feature functions receive an output mode and print through Click.
- Cute is the default output mode; Plain and JSON are also supported.
- Aliases are provided through Click's aliased group.
- CLI tests use Click's CliRunner and the standard-library unittest framework.

## Intended direction

The CLI remains the primary interface. Other interfaces may be added without making them prerequisites.

Potential interfaces:

- **CLI:** primary interface for utilities and interaction.
- **Shell integration:** optional adapter that can bring Kawa into the user's shell workflow.
- **TUI:** possible future interface for richer interaction.

## Conceptual components

As the project grows, it may be useful to keep these responsibilities distinct:

- **Command / interface layer:** parses input and presents results.
- **Core feature logic:** performs calculations and other useful work.
- **Character behavior:** defines Kawa's reactions and personality.
- **Interaction logic:** handles user interactions and relationship-related behavior.
- **State management:** reads and writes local user state.

These are conceptual boundaries, not a requirement to create a class, package, or abstraction for each item. Keep the implementation proportionate to the project's size.

## Local state

The intended direction is local-first. If persistent state is introduced, possible data includes:

- Mood.
- Bond / relationship.
- Relevant interaction history.
- User preferences.
- Day streak.

A local JSON file may be sufficient initially. The storage format and exact schema should be decided when implementation requirements are clearer.

Do not introduce persistent state merely because the architecture mentions it. Features should justify the complexity.

## Architectural constraints

- CLI utilities must remain usable without character state.
- JSON output must never contain character dialogue or decorative text.
- Shell integration must remain optional.
- Avoid unnecessary runtime dependencies.
- Preserve compatibility with supported packaging and distribution paths.
- Keep behavior testable and predictable.
- Do not split the code into layers or packages without a concrete benefit.

## Changing the architecture

When a change affects shared structure or introduces a new architectural pattern:

1. Explain the problem it solves.
2. Describe the proposed change and its trade-offs.
3. Check its impact on tests, packaging, and existing commands.
4. Get approval from the project owner before treating the direction as decided.

The architecture document should be updated when the actual implementation changes materially.
