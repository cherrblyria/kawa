import click
from importlib.resources import files

from .utils import *
from .modules import *

try:
    BANNER = files("kawa").joinpath("assets/banner.txt").read_text(encoding="utf-8")
except Exception:
    BANNER = "Oops!, seem like banner is missing..."

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(None, "-v", "--version", package_name="kawa")
def cli():
    """Useless cute little CLI tool"""
    pass


@cli.group()
def mc():
    """Minecraft tools"""
    pass


@mc.command()
@click.argument("x", type=float)
@click.argument("z", type=float)
def ntow(x, z):
    """Convert Nether coordinates to Overworld coordinates"""
    nether_to_overworld(x, z)


@mc.command()
@click.argument("x", type=float)
@click.argument("z", type=float)
def ownt(x, z):
    """Convert Overworld coordinates to Nether coordinates"""
    overworld_to_nether(x, z)


@cli.command(name="uwuify")
@click.argument("text", nargs=-1, required=True)
def uwuify_cmd(text):
    """Uwuify given text with uwuipy"""
    uwuify(list(text))


if __name__ == "__main__":
    cli()
