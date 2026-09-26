from uwuipy import Uwuipy


def uwuify(args):
    uwu = Uwuipy()
    uwuified = []
    for i, v in enumerate(args.text):
        uwuified.append(uwu.uwuify(args.text[i]))
    print(" ".join(uwuified))
