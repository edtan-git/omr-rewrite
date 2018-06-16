""" find circle and extract information from aligned sheet """

import os
import cv2
import imutils

DIR_PROCESSING_RESULT = 'processing_result'

DEFAULT_CIRCLE_MIN_WIDTH = 30
DEFAULT_CIRCLE_MAX_WIDTH = 32

DEFAULT_CIRCLE_MIN_HEIGHT = 29
DEFAULT_CIRCLE_MAX_HEIGHT = 33


def findCircle(image, options):
    """ find contour that listed as circle """
    image_copy = image.copy()
    image_copy = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image_name = options['image_name']

    contours = cv2.findContours(image, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]

    index = 0
    for (index, tmp_contour) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(tmp_contour)

        point = (tmp_contour[0][0][0], tmp_contour[0][0][1])

        if w >= DEFAULT_CIRCLE_MIN_WIDTH and w <= DEFAULT_CIRCLE_MAX_WIDTH and h >= DEFAULT_CIRCLE_MIN_HEIGHT and h <= DEFAULT_CIRCLE_MAX_HEIGHT:
            image_copy = cv2.drawContours(image_copy, [tmp_contour], -1, 255, -1)

        cv2.putText(image_copy, str(h) + ' ' + str(w),
                    point, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)

        index += 1

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'threshold_with_contour' + image_name + '.png'
        ),
        image_copy
    )
