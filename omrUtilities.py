""" handle omr basic function """

import cv2
import os
import numpy as np
from imutils import contours as imutils_contours
from math import atan2, degrees, pi

DEFAULT_THRESHOLD_AR_MIN = 0.958
DEFAULT_THRESHOLD_AR_MAX = 1.28

#DEFAULT_THRESHOLD_W_MIN = 31
#DEFAULT_THRESHOLD_W_MAX = 36

DEFAULT_THRESHOLD_W_MIN = 31
DEFAULT_THRESHOLD_W_MAX = 39

DEFAULT_THRESHOLD_H_MIN = 28
DEFAULT_THRESHOLD_H_MAX = 34

DEFAULT_WIDTH = 1700.0

DIR_PROCESSING_RESULT = 'processing_result'

def findBlackBoxAnchor(contours, options):
    """ find black box anchor """
    # square_box_indexes = [4, 2, 1063, 1046]
    # square_box_indexes = [1, 2, 1056, 1058]
    image = options['image']
    image_threshold = options['image_threshold']
    image_name = options['image_name']
    image_with_contour = image.copy()

    ratio = options['image_width'] / DEFAULT_WIDTH
    square_contours = list()
    square_attributes = list()

    ordered_square_contours = imutils_contours.sort_contours(
        contours, method="top-to-bottom"
    )
    ordered_square_contours = ordered_square_contours[0]

    for (j, tmp_contour) in enumerate(ordered_square_contours):
        (x, y, w, h) = cv2.boundingRect(tmp_contour)

        if h == 0:
            continue

        ar = w / float(h)
        threshold_w_min = DEFAULT_THRESHOLD_W_MIN * ratio
        threshold_w_max = DEFAULT_THRESHOLD_W_MAX * ratio
        threshold_h_min = DEFAULT_THRESHOLD_H_MIN * ratio
        threshold_h_max = DEFAULT_THRESHOLD_H_MAX * ratio

        is_threshold_ar_pass = ar >= DEFAULT_THRESHOLD_AR_MIN and ar <= DEFAULT_THRESHOLD_AR_MAX
        is_threshold_w_pass = w >= threshold_w_min and w <= threshold_w_max
        is_threshold_h_pass = h >= threshold_h_min and h <= threshold_h_max

        mask = np.zeros(image_threshold.shape, dtype="uint8")
        image_mask_temp = cv2.drawContours(mask, [tmp_contour], -1, 255, -1)

        mask = cv2.bitwise_and(image_threshold, image_threshold, mask=mask)
        total = cv2.countNonZero(mask)

        # if j in square_box_indexes:
        # if is_threshold_ar_pass and is_threshold_w_pass and is_threshold_h_pass:
        if is_threshold_ar_pass and is_threshold_w_pass and is_threshold_h_pass and total > 800:
            square_contours.append(tmp_contour)
            square_attributes.append((x, y, w, h))
            # cv2.imwrite(
            #     os.path.join(
            #         DIR_PROCESSING_RESULT,
            #         'image_mask_by_index-' + str(j) + image_name + '.png'
            #     ),
            #     image_mask_temp
            # )

            image_with_contour = cv2.putText(image_with_contour, 'cnz : ' + str(j) + ' ' + str(total) + ' ' + str(w) + ' ' + str(h),
                                             (int(x) - 80, int(y) + 20),
                                             cv2.FONT_HERSHEY_COMPLEX,
                                             0.5,
                                             (0, 0, 255),
                                             2
                                            )

    # square_contours = np.array(square_contours)

    ordered_square_contours = imutils_contours.sort_contours(
        square_contours, method="top-to-bottom"
    )
    ordered_square_contours = ordered_square_contours[0]

    index = 1
    for tmp_contour in ordered_square_contours:
        (x, y, w, h) = cv2.boundingRect(tmp_contour)
        image_with_contour = cv2.putText(image_with_contour, str(index),
                                         (int(x), int(y) + 100),
                                         cv2.FONT_HERSHEY_COMPLEX,
                                         0.5,
                                         (0, 0, 255),
                                         2
                                        )
        image_with_contour = cv2.rectangle(image_with_contour,
                                           (x, y),
                                           (x + w, y + h),
                                           (139, 0, 139),
                                           2
                                          )
        index = index + 1

    # cv2.imwrite(
    #     os.path.join(
    #         DIR_PROCESSING_RESULT,
    #         'image_with_contour-' + image_name + '.png'
    #     ),
    #     image_with_contour
    # )

    return {
        'ordered_square_contours': ordered_square_contours,
        'square_attributes': square_attributes
    }

def findDegreeBias(square_box_contours):
    """ find degree bias on the paper """
    rect_sb_1 = cv2.minAreaRect(square_box_contours[0])
    box_1 = np.int0(cv2.boxPoints(rect_sb_1))

    rect_sb_2 = cv2.minAreaRect(square_box_contours[1])
    box_2 = np.int0(cv2.boxPoints(rect_sb_2))

    point_1_1 = box_1[0]
    x1 = point_1_1[0]
    y1 = point_1_1[1]

    point_2_1 = box_2[0]
    x2 = point_2_1[0]
    y2 = point_2_1[1]

    dx = x2 - x1
    dy = y2 - y1

    rads = atan2(dy, dx)
    rads %= 2*pi
    degs = degrees(rads)

    if degs > 90:
        degs -= 180

    rotation_center = (x1, y1)
    rotation_matrix = findRotationMatrix(rotation_center, degs)

    return {
        'rotation_center': (x1, y1),
        'rotation_matrix': rotation_matrix,
        'degree_bias': degs
    }

def findRotationMatrix(rotation_center, degree):
    """ create rotation matrix """
    rotation_matrix = cv2.getRotationMatrix2D(rotation_center, degree, 1.0)
    return rotation_matrix

def rotateImage(image, rotation_matrix, options):
    """ rotate image """
    image_name = options['image_name']
    result_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'image_after_rotation-' + image_name + '.png'
        ),
        result_image
    )

    return result_image
