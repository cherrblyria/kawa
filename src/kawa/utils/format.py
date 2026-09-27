def no_dot_zero(v):
    if v.is_integer():
        return int(v)
    else:
        return v


def comma(v):
    if v.is_integer():
        return f"{int(v):,}"
    else:
        return f"{v:,.2f}"
