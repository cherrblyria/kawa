import click
from auto_click_auto import enable_click_shell_completion_option
from importlib.resources import files
from importlib.metadata import version as _version

from .utils import *
from .modules import *

try:
    BANNER = files("kawa").joinpath("assets/banner.txt").read_text(encoding="utf-8")
except Exception:
    BANNER = "Oops!, seem like banner is missing..."

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

try:
    __version__ = _version("kawa")
except Exception:
    __version__ = "unknown"


@click.group(context_settings=CONTEXT_SETTINGS)
@enable_click_shell_completion_option(program_name="kawa")
@click.version_option(
    __version__,
    "-v",
    "--version",
    package_name="kawa",
    message=f"""
{BANNER}\n
%(prog)s version %(version)s
""",
)
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
