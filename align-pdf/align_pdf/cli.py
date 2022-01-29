import logging

import click
import pathlib

logging.basicConfig(level=logging.NOTSET)

from align_pdf.convert.cli import convert_cli
from align_pdf.sheet.cli import line_align_cli, fft_align_cli

from align_pdf.convert.cli import convert
from align_pdf.sheet.fft_align import fft_align

@click.command(help="Convert pdf <-> images")
@click.option("--input", required=True, type=click.Path(path_type=pathlib.Path))
def align(input: pathlib.Path):
    convert(input)
    convert_in = input.with_suffix("")
    convert_out = pathlib.Path(convert_in.parent / (convert_in.name + "-aligned"))
    fft_align(convert_in, convert_out)
    convert(convert_out)

@click.group()
def cli():
    pass


cli.add_command(align, name="align")
cli.add_command(convert_cli, name="convert")
cli.add_command(line_align_cli, name="line-align")
cli.add_command(fft_align_cli, name="fft-align")

if __name__ == "__main__":
    cli()
