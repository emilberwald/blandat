import cv2


def rotate_image(image, angle):
    """rotate_image Rotate image along centroid

    :param [type] mat: Source image
    :param [type] angle: Counter-clockwise angle [degrees]
    :return [type]: Rotated image
    """
    height, width = image.shape[:2]
    centroid = (width / 2, height / 2)

    rotation_mat = cv2.getRotationMatrix2D(centroid, angle, 1.0)

    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    rotation_mat[0, 2] += bound_w / 2 - centroid[0]
    rotation_mat[1, 2] += bound_h / 2 - centroid[1]

    rotated_mat = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h), borderValue=(255, 255, 255))
    return rotated_mat
