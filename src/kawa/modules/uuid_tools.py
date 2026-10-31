import json
import uuid

import click

KAOMOJI = " /ᐠ‸⑅‸ ᐟ\\ﾉ"


def run_uuid(version=4, mode="cute"):
    value = str(uuid.uuid7() if version == 7 else uuid.uuid4())

    if mode == "json":
        click.echo(json.dumps({"uuid": value, "version": version}, ensure_ascii=False))
    elif mode == "plain":
        click.echo(value)
    else:
        click.echo(f"{value}{KAOMOJI}")
