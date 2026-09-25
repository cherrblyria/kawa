def fmt_float(v: float):
    if v.is_integer():
        return int(v)
    else:
        return v
