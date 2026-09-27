import click
from ..utils import *


def nether_to_overworld(x, z):
    ow_x = x * 8
    ow_z = z * 8

    click.echo(
        f"Nether: ({fmt_float(x)}, {fmt_float(z)})  (σ･ω･)σ  Overworld: ({fmt_float(ow_x)}, {fmt_float(ow_z)})"
    )


def overworld_to_nether(x, z):
    ow_x = x / 8
    ow_z = z / 8

    click.echo(
        f"Overworld: ({fmt_float(x)}, {fmt_float(z)})  (σ･ω･)σ  Nether: ({fmt_float(ow_x)}, {fmt_float(ow_z)})"
    )
