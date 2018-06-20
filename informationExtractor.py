""" find circle and extract information from aligned sheet """

import os
import cv2
import numpy as np
import imutils
from omrRelativeDistance import getSpecificSquarePoint
from omrRelativeDistance import getRealAreaPoint

DIR_PROCESSING_RESULT = 'processing_result'

# DEFAULT_CIRCLE_MIN_WIDTH = 29
# DEFAULT_CIRCLE_MAX_WIDTH = 33

DEFAULT_CIRCLE_MIN_WIDTH = 28
# DEFAULT_CIRCLE_MAX_WIDTH = 36
DEFAULT_CIRCLE_MAX_WIDTH = 40

DEFAULT_CIRCLE_MIN_HEIGHT = 28
# DEFAULT_CIRCLE_MAX_HEIGHT = 33
DEFAULT_CIRCLE_MAX_HEIGHT = 40

def findCircle(image, options):
    """ find contour that listed as circle """
    image_copy = image.copy()
    image_copy = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image_name = options['image_name']

    square_attributes = options['square_attributes']
    points = options['points']
    left_top_square_box = getSpecificSquarePoint('LT', square_attributes)
    real_area_points = getRealAreaPoint(left_top_square_box, points)
    populated_contours = {}

    contours = cv2.findContours(image, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]

    for (index, tmp_contour) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(tmp_contour)

        point = (tmp_contour[0][0][0], tmp_contour[0][0][1])

        if w >= DEFAULT_CIRCLE_MIN_WIDTH and w <= DEFAULT_CIRCLE_MAX_WIDTH and h >= DEFAULT_CIRCLE_MIN_HEIGHT and h <= DEFAULT_CIRCLE_MAX_HEIGHT:
            populated_contours = populateCircle(
                real_area_points,
                populated_contours,
                (x, y, x+w, y+h),
                tmp_contour
            )

        image_copy = cv2.drawContours(image_copy, [tmp_contour], -1, 255, -1)

        cv2.putText(image_copy, str(h),
                    point, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'threshold_with_contour' + image_name + '.png'
        ),
        image_copy
    )

    return populated_contours

def populateCircle(real_area_points, populated_contours, contour_area, contour):
    x_start = contour_area[0]
    y_start = contour_area[1]

    x_end = contour_area[2]
    y_end = contour_area[3]

    contour_points = [
        (x_start, y_start),
        (x_end, y_start),
        (x_end, y_end),
        (x_start, y_end)
    ]

    for real_area_point in real_area_points:
        index_name = real_area_point[2]
        area_x1 = real_area_point[0][0]
        area_y1 = real_area_point[0][1]
        area_x2 = real_area_point[1][0]
        area_y2 = real_area_point[1][1]

        for contour_point in contour_points:
            x = contour_point[0]
            y = contour_point[1]

            x_valid = (x >= area_x1) and (x <= area_x2)
            y_valid = (y >= area_y1) and (y <= area_y2)

            if x_valid and y_valid:
                if index_name in populated_contours:
                    populated_contours[index_name].append(contour)
                else:
                    populated_contours[index_name] = [contour]
                break

    return populated_contours

def extractCircledBubble(populated_contours, image, options):
    print "extractCircleBubble was called\n"
    color = [
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (255, 255, 0),
        (255, 0, 255)
    ]

    image_name = options['image_name']

    # print populated_contours
    for (j, index) in enumerate(populated_contours):
        populated_contour = populated_contours[index]
        if index == 'NAME':
            extractName(populated_contour, image)
        # for contour in populated_contour:
        #     image = cv2.drawContours(image, [contour], -1, color[j], -1)

    # cv2.imwrite(
    #     os.path.join(
    #         DIR_PROCESSING_RESULT,
    #         'image_populated_contour' + image_name + '.png'
    #     ),
    #     image
    # )

def extractName(contours, image_threshold):
    DATA_SORT = 'HORIZONTAL'
    DATA_LENGTH = 20
    DATA_OPTIONS_LENGTH = 26

    index = 1
    for contour in contours:
        mask = np.zeros(image_threshold.shape, dtype="uint8")
        image_mask_temp = cv2.drawContours(mask, [contour], -1, 255, -1)

        mask = cv2.bitwise_and(image_threshold, image_threshold, mask=mask)
        total = cv2.countNonZero(mask)
        total_contour = cv2.contourArea(contour)

        #calculate percentage
        percentage_covered = total/total_contour

        if (percentage_covered > 0.9):
            print "this is selected " + str(index) + ' ' + str(percentage_covered)

        index += 1
