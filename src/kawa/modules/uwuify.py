import click
from uwuipy import Uwuipy


def uwuify(text: list):
    uwu = Uwuipy()
    uwuified = []
    for i, v in enumerate(text):
        uwuified.append(uwu.uwuify(text[i]))
    click.echo(" ".join(uwuified))
