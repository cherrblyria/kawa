import json
import math

import click

from ..utils import *


def nether_to_overworld(x, z, mode="cute"):
    ow_x = no_dot_zero(x * 8)
    ow_z = no_dot_zero(z * 8)

    if mode == "json":
        click.echo(json.dumps({"x": ow_x, "z": ow_z}))
    elif mode == "plain":
        click.echo(f"{ow_x}, {ow_z}")
    else:
        click.echo(
            f"Nether: ({no_dot_zero(x)}, {no_dot_zero(z)})  (σ･ω･)σ  Overworld: ({ow_x}, {ow_z})"
        )


def overworld_to_nether(x, z, mode="cute"):
    ow_x = no_dot_zero(x / 8)
    ow_z = no_dot_zero(z / 8)

    if mode == "json":
        click.echo(json.dumps({"x": ow_x, "z": ow_z}))
    elif mode == "plain":
        click.echo(f"{ow_x}, {ow_z}")
    else:
        click.echo(
            f"Overworld: ({no_dot_zero(x)}, {no_dot_zero(z)})  (σ･ω･)σ  Nether: ({ow_x}, {ow_z})"
        )


def level_to_experience(level, mode="cute"):
    if level < 0:
        raise click.BadParameter("level must be non-negative", param_hint="level")

    if level <= 16:
        exp = level**2 + 6 * level
    elif level <= 31:
        exp = 2.5 * level**2 - 40.5 * level + 360
    else:
        exp = 4.5 * level**2 - 162.5 * level + 2220

    if mode == "json":
        click.echo(json.dumps({"level": level, "experience": no_dot_zero(exp)}))
    elif mode == "plain":
        click.echo(str(no_dot_zero(exp)))
    else:
        message = ""
        if level == 21863:
            message = "\\n - This's the maximum XP the game can handle btw :3"
        elif level > 21863:
            message = "\\n - I think this amount of XP can break the game :3"

        click.echo(f"Level: {comma(level)}  (σ≧∀≦)σ  Experience: {comma(exp)}{message}")


def experience_to_level(xp, mode="cute"):
    if xp < 0:
        raise click.BadParameter("xp must be non-negative", param_hint="xp")

    if xp <= 352:
        level = math.sqrt(xp + 9) - 3
    elif xp <= 1507:
        level = (81 / 10) + math.sqrt((2 / 5) * (xp - (7839 / 40)))
    else:
        level = (325 / 18) + math.sqrt((2 / 9) * (xp - (54215 / 72)))

    if mode == "json":
        click.echo(json.dumps({"experience": xp, "level": no_dot_zero(level)}))
    elif mode == "plain":
        click.echo(str(no_dot_zero(level)))
    else:
        message = ""
        if xp == 2147483647:
            message = "\\n - Have you ever reach this level before?"
        elif xp > 2147483647:
            message = "\\n - It's impossible to reach this level in survival btw :3"

        click.echo(f"Experience: {comma(xp)}  (σ≧∀≦)σ  Level: {comma(level)}{message}")
