import logging
import pathlib

import cv2
import numpy
import tqdm
from align_pdf.sheet.utils import rotate_image


def fft_align(input_path: pathlib.Path, output_path: pathlib.Path):
    for file_no, file in enumerate(
        tqdm.tqdm((sorted((file for file in input_path.glob("**/*") if file.is_file()), key=lambda path: str(path))))
    ):
        file: pathlib.Path
        output_path.mkdir(exist_ok=True)
        try:
            image = cv2.imread(str(file))
            image = align_image(image)
            image = crop_image(image, pad_on_left=(file_no % 2) == 1)
            cv2.imwrite(str(output_path / file.with_suffix(".png").name), image)
        except Exception as e:
            logging.error(e)


def crop_image(image, pad_on_left):
    is_color = len(image.shape) == 3
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if is_color else image

    _threshold, grayscale = cv2.threshold(grayscale, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    notePixelContours = cv2.findNonZero(255 - grayscale)
    x, y, w, h = cv2.boundingRect(notePixelContours)
    cropped_image = image[y : y + h, x : x + w]

    # A4 w 210 h 297
    # 1 cm margin above and below is ca 4% of height
    # margin should be 20-25 mm, 10% of width for holes
    vertical = int(0.04 * h)
    left = int(0.1 * w) if pad_on_left else 0
    right = int(0.1 * w) if not pad_on_left else 0
    cropped_image = cv2.copyMakeBorder(
        cropped_image, vertical, vertical, left, right, cv2.BORDER_CONSTANT, value=(255, 255, 255) if is_color else 255
    )

    return cropped_image


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
