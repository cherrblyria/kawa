import argparse


def nether_to_overworld(args):
    ow_x = args.x * 8
    ow_z = args.z * 8

    fmt = lambda v: int(v) if v.is_integer() else v
    print(
        f"Nether: ({fmt(args.x)}, {fmt(args.z)})  (σ･ω･)σ  Overworld: ({fmt(ow_x)}, {fmt(ow_z)})"
    )


def overworld_to_nether(args):
    ow_x = args.x / 8
    ow_z = args.z / 8

    fmt = lambda v: int(v) if v.is_integer() else v
    print(
        f"Overworld: ({fmt(args.x)}, {fmt(args.z)})  (σ･ω･)σ  Nether: ({fmt(ow_x)}, {fmt(ow_z)})"
    )


def main():
    kawa_parser = argparse.ArgumentParser(
        prog="kawa", description="Use less cute little CLI tool"
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

    args = kawa_parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
