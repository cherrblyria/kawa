import functools
import json

import click
from uwuipy import Uwuipy


@functools.cache
def get_uwu():
    return Uwuipy()


def run_uwuify(text: list, mode="cute"):
    uwu = get_uwu()
    uwuified = []
    for i, v in enumerate(text):
        uwuified.append(uwu.uwuify(v))
    result = " ".join(uwuified)
    if mode == "json":
        click.echo(json.dumps({"result": result}, ensure_ascii=False))
    else:
        click.echo(result)
