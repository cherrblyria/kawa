import argparse
import argcomplete
from importlib.resources import files

from .utils import *
from .modules import *

try:
    BANNER = files("kawa").joinpath("assets/banner.txt").read_text(encoding="utf-8")
except Exception:
    BANNER = "Oops!, seem like banner is missing..."


class BannerArgumentParser(argparse.ArgumentParser):
    def format_help(self):
        formatter = self._get_formatter()

        if BANNER:
            formatter.add_text(BANNER)

        formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)

        formatter.add_text(self.description)

        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        formatter.add_text(self.epilog)

        return formatter.format_help()


def main():
    kawa_parser = BannerArgumentParser(
        prog="kawa",
        description=f"  - Useless cute little CLI tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    kawa_subparsers = kawa_parser.add_subparsers(dest="tool", required=True)

    # kawa mc ...
    mc_parser = kawa_subparsers.add_parser("mc", help="Minecraft tools")
    mc_subparsers = mc_parser.add_subparsers(dest="command", required=True)

    # kawa mc ntow <x> <z>
    mc_ntow_parser = mc_subparsers.add_parser(
        "ntow", help="Convert Nether coordinates to Overworld coordinates"
    )
    mc_ntow_parser.add_argument("x", type=float, help="Nether X coordinate")
    mc_ntow_parser.add_argument("z", type=float, help="Nether Z coordinate")
    mc_ntow_parser.set_defaults(func=nether_to_overworld)

    # kawa mc ownt <x> <z>
    mc_ownt_parser = mc_subparsers.add_parser(
        "ownt", help="Convert Overworld coordinates to Nether coordinates"
    )
    mc_ownt_parser.add_argument("x", type=float, help="Overworld X coordinate")
    mc_ownt_parser.add_argument("z", type=float, help="Overworld Z coordinate")
    mc_ownt_parser.set_defaults(func=overworld_to_nether)

    # kawa uwuify
    uwu_parser = kawa_subparsers.add_parser(
        "uwuify", help="Uwuify given text with uwuipy"
    )
    uwu_parser.add_argument("text", type=str, help="Text to convert")
    uwu_parser.set_defaults(func=uwuify)

    argcomplete.autocomplete(kawa_parser)
    args = kawa_parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
