import logging
import pathlib

import click
import pdf2image
import PIL
import PIL.Image


@click.command(help="Convert pdf <-> images")
@click.option("--input", required=True, type=click.Path(path_type=pathlib.Path))
def convert_cli(input: pathlib.Path):
    if input.is_file() and input.suffix == ".pdf":
        output = input.with_suffix("")
        output.mkdir(exist_ok=False)
        logging.info(f"Convert {input} to images in {output} ...")
        pdf2image.convert_from_path(str(input), output_folder=output)
    elif input.is_dir():
        output = input.with_suffix(".pdf")
        assert not output.exists()
        logging.info(f"Convert images in {input} to {output} ...")
        pil_images = list()
        for file in sorted((file for file in input.glob("**/*") if file.is_file()), key=lambda path: str(path)):
            try:
                pil_image = PIL.Image.open(str(file))
                pil_images.append(pil_image)
            except:
                pass
        pil_images[0].save(str(output), save_all=True, append_images=pil_images[1:])
    else:
        raise ValueError(f"not clear how to convert {input}.")
