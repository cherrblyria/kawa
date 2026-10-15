import json
from pathlib import Path

import click

JSON_STARTS = (
    "{",
    "[",
    '"',
    "t",
    "f",
    "n",
    "-",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
)


def pretty_json(
    source: str, indent: int = 4, sort_keys: bool = False, mode: str = "cute"
) -> None:
    # Output is valid JSON in every mode, so mode only affects nothing — flags
    # are accepted for consistency with the rest of the CLI.
    path = Path(source)

    if path.is_file():
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError as e:
            raise click.ClickException(f"Can't read {source}: {e}") from e
    else:
        raw = source

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        if not path.is_file() and (
            source.endswith(".json") or not raw.lstrip().startswith(JSON_STARTS)
        ):
            raise click.ClickException(f"File not found: {source}") from e
        raise click.ClickException(f"Invalid JSON: {e}") from e

    click.echo(json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False))
