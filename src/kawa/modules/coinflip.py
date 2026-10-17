import functools
import json
import random
from time import localtime

import click
from uwuipy import Uwuipy

COINS_MESSAGES = [
    "!",
    "?",
    "!?",
    "~ Nya~",
    "! That's it",
    ", I think so..",
    "! As I expected..",
    ".. This one is good right?",
]

KAWA_MESSAGES = [
    "I dunno I just ate it :3",
    "NYA?",
    "The coins just flew away..",
    "Ummmm, I lost it..",
    "Wait a minute.. I just dropped it...",
]

SECRET_PLACEHOLDER_MESSAGES = [
    "nutty the dev: Oops, This thing's still WIP",
    "nutty the dev: Umm... I think you shouldn't see this...",
    "nutty the dev: Woah... this's super rare but.. it's not done yet.",
    "Why am I here!?...",
]

EASTER_EGG_EVENTS = [
    {
        "name": "kawa",
        "chance": 1 / 100,
        "messages": KAWA_MESSAGES,
    },
    {
        "name": "secret",
        "chance": 1 / 100_000,
        "messages": SECRET_PLACEHOLDER_MESSAGES,
    },
]


@functools.cache
def get_uwu():
    return Uwuipy()


def pick_event(mode, rng=None):
    if mode != "cute":
        return None
    if rng is None:
        rng = random.Random()
    for event in EASTER_EGG_EVENTS:
        if rng.random() < event["chance"]:
            return event
    return None


def run_coinflip(hour=None, mode="cute", rng=None):
    if hour is None:
        hour = localtime().tm_hour
    if rng is None:
        rng = random.Random()
    heads_bias = 0.51 if hour < 12 else 0.49
    side = "Heads" if rng.random() < heads_bias else "Tails"
    event = pick_event(mode, rng)
    if event is not None:
        message = rng.choice(event["messages"])
        if event["name"] == "kawa":
            message = get_uwu().uwuify(message)
    elif mode == "cute":
        message = get_uwu().uwuify(rng.choice(COINS_MESSAGES))
    elif mode == "json":
        message = rng.choice(COINS_MESSAGES)
    else:
        message = ""
    if mode == "json":
        click.echo(
            json.dumps({"result": side.lower(), "message": message}, ensure_ascii=False)
        )
    elif mode == "plain":
        click.echo(side.lower())
    elif event is None:
        click.echo(f"{side}{message}")
    else:
        click.echo(f"{message}")
