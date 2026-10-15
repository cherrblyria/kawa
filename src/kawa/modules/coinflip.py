import json
import random
from time import localtime

import click

HEADS_MESSAGES = [
    "The universe has chosen for you.",
    "Mochi says yes.",
    "Fate feels generous today.",
    "The stars aligned~",
]

TAILS_MESSAGES = [
    "The cat says nope.",
    "Mochi disagrees.",
    "Fate is feeling chaotic.",
    "Not today, comrade~",
]


def coinflip(hour=None, mode="cute"):
    if hour is None:
        hour = localtime().tm_hour

    heads_bias = 0.51 if hour < 12 else 0.49  # AM: 51/49, PM: 49/51

    if random.random() < heads_bias:
        side, message = "Heads", random.choice(HEADS_MESSAGES)
    else:
        side, message = "Tails", random.choice(TAILS_MESSAGES)

    if mode == "json":
        click.echo(
            json.dumps({"result": side.lower(), "message": message}, ensure_ascii=False)
        )
    elif mode == "plain":
        click.echo(side.lower())
    else:
        click.echo(f"{side}! {message}")
