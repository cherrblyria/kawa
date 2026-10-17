import json
import math
import sys
from pathlib import Path

import click


def reject_nonstandard(value):
    raise ValueError(f"{value} is not allowed")


def track_duplicates(pairs):
    seen = set()
    result = {}
    for key, value in pairs:
        if key in seen:
            click.echo(f"Warning: duplicate key {key!r}", err=True)
        seen.add(key)
        result[key] = value
    return result


def looks_like_path(raw):
    stripped = raw.strip()
    if stripped[:1] in ("{", "[", '"'):
        return False
    if "/" in raw or "\\" in raw:
        return True
    if stripped.endswith(".json"):
        return True
    return "." in stripped and " " not in stripped


def pretty_json(
    source: str, indent: int = 4, sort_keys: bool = False, mode: str = "cute"
) -> None:
    if source == "-":
        try:
            raw = sys.stdin.read()
        except OSError as e:
            raise click.ClickException(f"Can't read stdin: {e}") from e
        from_file = False
    else:
        path = Path(source)
        if path.is_symlink() and not path.exists():
            raise click.ClickException(f"Broken symlink: {source}")
        if path.exists() and not path.is_file():
            if path.is_dir():
                raise click.ClickException(f"{source} is a directory")
            raise click.ClickException(f"Can't read {source}: not a file")
        if path.is_file():
            try:
                raw = path.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError as e:
                raise click.ClickException(f"Can't read {source}: {e}") from e
            except OSError as e:
                raise click.ClickException(f"Can't read {source}: {e}") from e
            from_file = True
        else:
            raw = source
            from_file = False
    try:
        data = json.loads(
            raw,
            object_pairs_hook=track_duplicates,
            parse_constant=reject_nonstandard,
            parse_float=lambda v: (
                float(v) if math.isfinite(float(v)) else reject_nonstandard(v)
            ),
            parse_int=lambda v: int(v),
        )
    except RecursionError as e:
        raise click.ClickException(f"Invalid JSON: {e}") from e
    except ValueError as e:
        if not from_file and looks_like_path(source):
            raise click.ClickException(f"File not found: {source}") from e
        raise click.ClickException(f"Invalid JSON: {e}") from e
    try:
        text = json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
    except UnicodeEncodeError:
        text = json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=True)
    except (ValueError, RecursionError) as e:
        raise click.ClickException(f"Invalid JSON: {e}") from e
    try:
        click.echo(text)
    except UnicodeEncodeError:
        click.echo(
            json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=True)
        )
