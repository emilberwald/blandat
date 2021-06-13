import cmath
import logging
import math
import pathlib

import cv2
import tqdm

from align_pdf.sheet.utils import rotate_image


def line_align(input_path: pathlib.Path, output_path: pathlib.Path):
    for file in tqdm.tqdm(
        (sorted((file for file in input_path.glob("**/*") if file.is_file()), key=lambda path: str(path)))
    ):
        file: pathlib.Path
        try:
            image = cv2.imread(str(file))
            image = align_image(image)
            cv2.imwrite(str(output_path / file.with_suffix(".png").name), image)
        except Exception as e:
            logging.error(e)


def find_rotation(image):
    """find_rotation Find rotation to get image aligned

    :param [type] image: Image
    :return [type]: Suggested rotation
    """
    # https://stackoverflow.com/a/16047590/3021108
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_high, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    threshold_low = 0.5 * threshold_high
    edge_image = cv2.Canny(image, int(threshold_low), int(threshold_high))
    # black ink on white paper
    # edge_image = threshold_image.max() - threshold_image
    # debug_image = cv2.cvtColor(edge_image, cv2.COLOR_GRAY2BGR)

    height, width, channels = image.shape
    accumulator_distance_resolution_px = 1
    accumulator_angle_resolution_radians = math.radians(0.1)
    accumulator_vote_threshold = 100
    accumulator_min_line_length = int(width * 0.5)
    accumulator_max_line_gap = int(width * 0.05)
    if (
        lines := cv2.HoughLinesP(
            edge_image,
            accumulator_distance_resolution_px,
            accumulator_angle_resolution_radians,
            accumulator_vote_threshold,
            minLineLength=accumulator_min_line_length,
            maxLineGap=accumulator_max_line_gap,
        )
    ) is not None:
        rotations = list()
        for x0, y0, x1, y1 in (line[0] for line in lines):
            dy = y1 - y0
            dx = x1 - x0
            angle = math.atan2(dy, dx)
            rotations.append(angle)
            # cv2.line(debug_image, (x0, y0), (x1, y1), (0, 0, 255), thickness=1)
        # cv2.imwrite("debug_image.png", debug_image)
        return math.degrees(mean_angle(rotations)) if rotations else None
    return None


def mean_angle(angle):
    return cmath.phase(sum(cmath.rect(1, d) for d in angle) / len(angle))


def align_image(image):
    """align_image align image

    :param [type] image: OpenCV image (BGR)
    :return [type]: Aligned image (BGR)
    """
    if (rotation := find_rotation(image)) is not None:
        if abs(rotation) > 0.01:
            return rotate_image(image, rotation)
    return image
