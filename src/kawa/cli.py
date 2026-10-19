import functools
import math
import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version
from importlib.resources import files

import click
from auto_click_auto import enable_click_shell_completion_option
from click_aliases import ClickAliasedGroup

from .modules import *
from .utils import *

try:
    BANNER = files("kawa").joinpath("assets/banner.txt").read_text(encoding="utf-8")
except OSError:
    BANNER = "Oops!, seem like banner is missing..."

for stream in (sys.stdout, sys.stderr):
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except ValueError:
            pass

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}

MC_CONTEXT_SETTINGS = {
    "ignore_unknown_options": True,
    "help_option_names": ["-h", "--help"],
}


class FiniteFloat(click.ParamType):
    name = "float"

    def convert(self, value, param, ctx):
        try:
            result = float(value)
        except TypeError, ValueError:
            self.fail(f"{value!r} is not a valid float", param, ctx)
        if not math.isfinite(result):
            self.fail("must be a finite number", param, ctx)
        return result


try:
    __version__ = _version("kawa")
except PackageNotFoundError:
    __version__ = "unknown"


def output_mode(func):
    """Attach --json/--plain flags; mode resolves leaf flag > group flag > cute."""

    @click.option(
        "--json", "output_json", is_flag=True, help="Output machine-readable JSON"
    )
    @click.option(
        "--plain",
        "output_plain",
        is_flag=True,
        help="Output plain result, no decoration",
    )
    @functools.wraps(func)
    def wrapper(*args, output_json, output_plain, **kwargs):
        if output_json and output_plain:
            raise click.UsageError("--json and --plain are mutually exclusive")
        ctx = click.get_current_context()
        inherited = (ctx.obj or {}).get("output", "cute")
        mode = "json" if output_json else "plain" if output_plain else inherited
        ctx.obj = {"output": mode}
        return func(*args, mode=mode, **kwargs)

    return wrapper


@click.group(context_settings=CONTEXT_SETTINGS, cls=ClickAliasedGroup)
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
@output_mode
def cli(mode):
    """Useless cute little CLI tool"""


@cli.group(aliases=["mc"], cls=ClickAliasedGroup)
@output_mode
def minecraft(mode):
    """Minecraft tools"""


@minecraft.command(context_settings=MC_CONTEXT_SETTINGS, aliases=["ntow", "nt"])
@click.argument("x", type=FiniteFloat())
@click.argument("z", type=FiniteFloat())
@output_mode
def nether(x, z, mode):
    """Convert Nether coordinates to Overworld coordinates"""
    nether_to_overworld(x, z, mode)


@minecraft.command(context_settings=MC_CONTEXT_SETTINGS, aliases=["ownt", "ow"])
@click.argument("x", type=FiniteFloat())
@click.argument("z", type=FiniteFloat())
@output_mode
def overworld(x, z, mode):
    """Convert Overworld coordinates to Nether coordinates"""
    overworld_to_nether(x, z, mode)


@minecraft.command(context_settings=MC_CONTEXT_SETTINGS, aliases=["lvxp", "lv"])
@click.argument("level", type=click.IntRange(min=0, max=10**9))
@output_mode
def level(level, mode):
    """Convert Level to Experience"""
    level_to_experience(level, mode)


@minecraft.command(context_settings=MC_CONTEXT_SETTINGS, aliases=["xplv", "xp"])
@click.argument("xp", type=click.IntRange(min=0, max=10**18))
@output_mode
def xp(xp, mode):
    """Convert Experience to Level"""
    experience_to_level(xp, mode)


@cli.command(name="uwuify", aliases=["uwu"])
@click.argument("text", nargs=-1, required=True)
@output_mode
def uwuify_cmd(text, mode):
    """Uwuify given text with uwuipy"""
    run_uwuify(list(text), mode)


@cli.command(name="coinflip", aliases=["cf"])
@output_mode
def coinflip_cmd(mode):
    """Flip a coin"""
    run_coinflip(mode=mode)


@cli.group(name="json")
@output_mode
def json_group(mode):
    """JSON tools"""


@json_group.command()
@click.argument("source")
@click.option(
    "-i", "--indent", type=click.IntRange(min=0, max=16), default=4, show_default=True
)
@click.option("-s", "--sort-keys", is_flag=True)
@output_mode
def pretty(source, indent, sort_keys, mode):
    """Pretty-print JSON from a file path or raw string"""
    pretty_json(source, indent, sort_keys, mode)


if __name__ == "__main__":
    cli()
