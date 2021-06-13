import pathlib

import click
from align_pdf.sheet.line_align import line_align
from align_pdf.sheet.fft_align import fft_align


@click.command(help="Aligns images along long lines")
@click.option("--input", required=True, type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option("--output", required=True, type=click.Path(file_okay=False, path_type=pathlib.Path))
def line_align_cli(input, output):
    line_align(input, output)


@click.command(help="Aligns images using fft")
@click.option("--input", required=True, type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option("--output", required=True, type=click.Path(file_okay=False, path_type=pathlib.Path))
def fft_align_cli(input, output):
    fft_align(input, output)
