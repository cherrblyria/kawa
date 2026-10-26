import json
import math
import random

import click

from ..utils import *

BORDER_MESSAGE = [
    "\n - Well, that's past the world border, good luck getting there :3",
    "\n - Are you going to build your base there??",
    "\n - Have you ever reach that?",
    "\n - Let's go Farland :3",
]


def exp_for_level(level):
    if level <= 16:
        return level**2 + 6 * level
    elif level <= 31:
        return (5 * level**2 - 81 * level + 720) // 2
    else:
        return (9 * level**2 - 325 * level + 4440) // 2


def check_finite(value):
    if not math.isfinite(value):
        raise click.BadParameter("must be a finite number")


def check_overflow(value):
    if not math.isfinite(value):
        raise click.BadParameter("result out of range")


def nether_to_overworld(x, z, mode="cute", rng=None):
    check_finite(x)
    check_finite(z)
    raw_x = x * 8
    raw_z = z * 8

    check_overflow(raw_x)
    check_overflow(raw_z)
    ow_x = no_dot_zero(raw_x)
    ow_z = no_dot_zero(raw_z)

    if rng is None:
        rng = random.Random()

    if mode == "json":
        click.echo(json.dumps({"x": ow_x, "z": ow_z}, allow_nan=False))
    elif mode == "plain":
        click.echo(f"{ow_x}, {ow_z}")
    else:
        border = ""
        if abs(x) > 30000000 or abs(z) > 30000000:
            border = rng.choice(BORDER_MESSAGE)
        click.echo(
            f"(x: {no_dot_zero(x)} y: {no_dot_zero(z)}) in Nether is (x: {ow_x} y: {ow_z}) in Overworld  /ᐠ｡ꞈ｡ᐟ\\{border}"
        )


def overworld_to_nether(x, z, mode="cute", rng=None):
    check_finite(x)
    check_finite(z)
    raw_x = x / 8
    raw_z = z / 8

    check_overflow(raw_x)
    check_overflow(raw_z)
    ow_x = no_dot_zero(raw_x)
    ow_z = no_dot_zero(raw_z)

    if rng is None:
        rng = random.Random()

    if mode == "json":
        click.echo(json.dumps({"x": ow_x, "z": ow_z}, allow_nan=False))
    elif mode == "plain":
        click.echo(f"{ow_x}, {ow_z}")
    else:
        border = ""
        if abs(x) > 30000000 or abs(z) > 30000000:
            border = rng.choice(BORDER_MESSAGE)
        click.echo(
            f"(x: {no_dot_zero(x)} y: {no_dot_zero(z)}) in Overworld is (x: {ow_x} y: {ow_z}) in Nether  /ᐠ｡ꞈ｡ᐟ\\{border}"
        )


def level_to_experience(level, mode="cute"):
    if level < 0:
        raise click.BadParameter("level must be non-negative", param_hint="level")

    xp = exp_for_level(level)
    if mode == "json":
        click.echo(json.dumps({"level": level, "experience": no_dot_zero(xp)}))
    elif mode == "plain":
        click.echo(str(no_dot_zero(xp)))
    else:
        message = ""
        if level == 21863:
            message = "\n - This's the maximum XP the game can handle btw :3"
        elif level > 21863:
            message = "\n - I think this amount of XP can break the game :3"
        click.echo(f"Level {comma(level)} is {comma(xp)} Experience /ᐠ｡‸｡ᐟ\\{message}")


def experience_to_level(xp, mode="cute"):
    if xp < 0:
        raise click.BadParameter("xp must be non-negative", param_hint="xp")

    if xp <= 352:
        level = math.sqrt(xp + 9) - 3
    elif xp <= 1507:
        level = (81 / 10) + math.sqrt((2 / 5) * (xp - (7839 / 40)))
    else:
        level = (325 / 18) + math.sqrt((2 / 9) * (xp - (54215 / 72)))

    candidate = round(level)
    if candidate >= 0 and exp_for_level(candidate) == xp:
        level = candidate

    if mode == "json":
        click.echo(json.dumps({"experience": xp, "level": no_dot_zero(level)}))
    elif mode == "plain":
        click.echo(str(no_dot_zero(level)))
    else:
        message = ""
        if xp == 2147483647:
            message = "\n - Have you ever reach this level before?"
        elif xp > 2147483647:
            message = "\n - It's impossible to reach this level in survival btw :3"
        click.echo(f"{comma(xp)} Experience is Level {comma(level)} /ᐠ｡‸｡ᐟ\\{message}")


STORAGE_LABELS = {
    "item": "item(s)",
    "stack": "stack(s)",
    "shulker": "shulker box(es)",
    "large_chest": "large chest(s)",
}


def convert_storage(
    amount, source, target, stack_size=64, large_chest=False, mode="cute"
):
    if target == "sb":
        target = "shulker"
    if source == "sb":
        source = "shulker"
    slots = 54 if large_chest else 27
    sizes = {
        "item": 1,
        "stack": stack_size,
        "shulker": slots * stack_size,
    }
    items = amount * sizes[source]
    target_size = sizes[target]
    quotient, remainder = divmod(items, target_size)
    whole = remainder == 0
    try:
        result = quotient if whole else items / target_size
    except OverflowError as exc:
        raise click.BadParameter("result too large") from exc
    container = (
        "large_chest"
        if large_chest and (source == "shulker" or target == "shulker")
        else "shulker_box"
    )
    payload = {
        "result": result,
        "from": source,
        "to": target,
        "amount": amount,
        "stack_size": stack_size,
        "container": container,
    }
    breakdown = {}
    if not whole:
        remaining = items
        for unit in ("shulker", "stack", "item"):
            count, remaining = divmod(remaining, sizes[unit])
            if count:
                breakdown[unit] = count
        payload["breakdown"] = {
            ("large_chest" if large_chest and unit == "shulker" else unit): count
            for unit, count in breakdown.items()
        }
    try:
        if mode == "json":
            click.echo(json.dumps(payload))
        elif mode == "plain":
            click.echo(str(result) if not whole else str(quotient))
        elif whole:
            label = (
                STORAGE_LABELS["large_chest"]
                if target == "shulker" and large_chest
                else STORAGE_LABELS[target]
            )
            suffix = " of item(s)" if target in ("stack", "shulker") else ""
            click.echo(f"that's {comma(quotient)} {label}{suffix} /ᐠ_ ꞈ _ᐟ\\ɴʏᴀ~")
        else:
            labels = {
                "shulker": (
                    STORAGE_LABELS["large_chest"]
                    if large_chest
                    else STORAGE_LABELS["shulker"]
                ),
                "stack": STORAGE_LABELS["stack"],
                "item": STORAGE_LABELS["item"],
            }
            parts = [
                f"{comma(count)} {labels[unit]}" for unit, count in breakdown.items()
            ]
            if len(parts) == 1:
                joined = parts[0]
            elif len(parts) == 2:
                joined = " and ".join(parts)
            else:
                joined = ", ".join(parts[:-1]) + " and " + parts[-1]
            click.echo(f"that's {joined} /ᐠ_ ꞈ _ᐟ\\ɴʏᴀ~")
    except (ValueError, OverflowError) as exc:
        raise click.BadParameter("result too large") from exc
