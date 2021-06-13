import logging

import click

logging.basicConfig(level=logging.NOTSET)

from align_pdf.convert.cli import convert_cli
from align_pdf.sheet.cli import line_align_cli, fft_align_cli


@click.group()
def cli():
    pass


cli.add_command(convert_cli, name="convert")
cli.add_command(line_align_cli, name="line-align")
cli.add_command(fft_align_cli, name="fft-align")

if __name__ == "__main__":
    cli()
