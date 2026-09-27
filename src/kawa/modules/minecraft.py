import click
import math
from ..utils import *


def nether_to_overworld(x, z):
    ow_x = x * 8
    ow_z = z * 8

    click.echo(
        f"Nether: ({no_dot_zero(x)}, {no_dot_zero(z)})  (σ･ω･)σ  Overworld: ({no_dot_zero(ow_x)}, {no_dot_zero(ow_z)})"
    )


def overworld_to_nether(x, z):
    ow_x = x / 8
    ow_z = z / 8

    click.echo(
        f"Overworld: ({no_dot_zero(x)}, {no_dot_zero(z)})  (σ･ω･)σ  Nether: ({no_dot_zero(ow_x)}, {no_dot_zero(ow_z)})"
    )


def level_to_experience(level):
    if level <= 16:
        click.echo(
            f"Level: {comma(level)}  (σ≧∀≦)σ  Expreience: {comma(level**2 + 6 * level)}"
        )
    elif level <= 31:
        click.echo(
            f"Level: {comma(level)}  (σ≧∀≦)σ  Expreience: {comma(2.5 * level**2 - 40.5 * level + 360)}"
        )
    else:
        message = ""
        if level == 21863:
            message = "\n\n - This's the maximum XP the game can handle btw :3"
        elif level > 21863:
            message = "\n\n - I think this amount of XP can break the game :3"

        click.echo(
            f"Level: {comma(level)}  (σ≧∀≦)σ  Expreience: {comma(4.5 * level**2 - 162.5 * level + 2220)}{message}"
        )


def experience_to_level(xp):
    if xp <= 352:
        click.echo(
            f"Expreience: {comma(xp)}  (σ≧∀≦)σ  Level: {comma(math.sqrt(xp+9)-3)}"
        )
    elif xp <= 1507:
        click.echo(
            f"Expreience: {comma(xp)}  (σ≧∀≦)σ  Level: {comma((81/10)+math.sqrt((2/5)*(xp-(7839/40))))}"
        )
    else:
        message = ""
        if xp == 2147483647:
            message = "\n\n - Have you ever reach this level before?"
        elif xp > 2147483647:
            message = "\n\n - It's impossible to reach this level in survival btw :3"

        click.echo(
            f"Expreience: {comma(xp)}  (σ≧∀≦)σ  Level: {comma((325/18)+math.sqrt((2/9)*(xp-(54215/72))))}{message}"
        )
