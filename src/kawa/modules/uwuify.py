import json

from uwuipy import Uwuipy


def uwuify(text: list, mode="cute"):
    uwu = Uwuipy()
    uwuified = []
    for i, v in enumerate(text):
        uwuified.append(uwu.uwuify(v))
    result = " ".join(uwuified)

    if mode == "json":
        return json.dumps({"result": result}, ensure_ascii=False)
    else:
        return result
