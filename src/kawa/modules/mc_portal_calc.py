from ..utils import *


def nether_to_overworld(args):
    ow_x = args.x * 8
    ow_z = args.z * 8

    print(
        f"Nether: ({fmt_float(args.x)}, {fmt_float(args.z)})  (σ･ω･)σ  Overworld: ({fmt_float(ow_x)}, {fmt_float(ow_z)})"
    )


def overworld_to_nether(args):
    ow_x = args.x / 8
    ow_z = args.z / 8

    print(
        f"Overworld: ({fmt_float(args.x)}, {fmt_float(args.z)})  (σ･ω･)σ  Nether: ({fmt_float(ow_x)}, {fmt_float(ow_z)})"
    )
