import logging
import pathlib

import cv2
import numpy
import tqdm
from align_pdf.sheet.utils import rotate_image


def fft_align(input_path: pathlib.Path, output_path: pathlib.Path):
    for file in tqdm.tqdm(
        (sorted((file for file in input_path.glob("**/*") if file.is_file()), key=lambda path: str(path)))
    ):
        file: pathlib.Path
        output_path.mkdir(exist_ok=True)
        try:
            image = cv2.imread(str(file))
            image = align_image(image)
            cv2.imwrite(str(output_path / file.with_suffix(".png").name), image)
        except Exception as e:
            logging.error(e)


def align_image(image):
    """align_image align image

    :param [type] image: OpenCV image (BGR)
    :return [type]: Aligned image (BGR)
    """
    if (rotation := find_rotation(image)) is not None:
        if abs(rotation) > 0.01:
            return rotate_image(image, rotation)
    return image


def find_rotation(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fourier = numpy.log(numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(gray_image))))
    height, width = gray_image.shape[:2]
    centroid = (width / 2, height / 2)
    fourier_polar = cv2.linearPolar(fourier, centroid, min(centroid), cv2.INTER_LINEAR + cv2.WARP_FILL_OUTLIERS)
    angle_histogram = numpy.mean(fourier_polar, axis=1)
    angle = 360 * numpy.argmax(angle_histogram) / len(angle_histogram)
    angle = angle + 90 - 180
    return angle if abs(angle) < 90 else angle - 180
