""" find circle and extract information from aligned sheet """

import os
import cv2
import imutils
import math

from omrRelativeDistance import getSpecificSquarePoint
from omrRelativeDistance import getRealAreaPoint

from sortPopulatedContours import sortPopulatedContours

from extractorLib import extractName, extractStudentNumber
from extractorLib import extractDateOfBirth, extractPackageNumber
from extractorLib import extractAnswerSheet

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
                contour_distance = calculateContourDistance(
                    (area_x1, area_y1),
                    (x_start, y_start)
                )

                if index_name in populated_contours:
                    counter = len(populated_contours[index_name]['contour_distances'])
                    populated_contours[index_name]['contours'].append(contour)
                    populated_contours[index_name]['contour_distances'].append((counter, contour_distance))
                else:
                    populated_contours[index_name] = {}
                    populated_contours[index_name]['contours'] = list()
                    populated_contours[index_name]['contour_distances'] = list()
                    populated_contours[index_name]['contours'].append(contour)
                    populated_contours[index_name]['contour_distances'].append((0, contour_distance))
                break

    return populated_contours

def extractCircledBubble(populated_contours, image, options):
    """ choose what function should be called based """
    print "extractCircleBubble was called\n"
    color = [
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (255, 255, 0),
        (255, 0, 255)
    ]

    image_name = options['image_name']
    image_color = image.copy()
    image_color = cv2.cvtColor(image_color, cv2.COLOR_GRAY2RGB)

    # populated_contours = sortPopulatedContours(populated_contours, image)
    # print populated_contours
    image_checker = image_color.copy()
    for (j, index) in enumerate(populated_contours):
        populated_contour = populated_contours[index]

        if index == 'NAME':
            contours = sortLeftToRightContours(populated_contour['contours'])
            image_checker = extractName(contours, image_checker)
        elif index == 'STUDENT_NUMBER':
            contours = sortLeftToRightContours(populated_contour['contours'])
            image_checker = extractStudentNumber(contours, image_checker)
        elif index == 'DATE_OF_BIRTH':
            contours = sortLeftToRightContours(populated_contour['contours'])
            image_checker = extractDateOfBirth(contours, image_checker)
        elif index == 'PACKAGE_NUMBER':
            contours = sortLeftToRightContours(populated_contour['contours'])
            image_checker = extractPackageNumber(contours, image_checker)
        elif index == 'ANSWER':
            contours = populated_contour['contours']
            image_checker = extractAnswerSheet(contours, image_checker)

        for contour in populated_contour['contours']:
            image_color = cv2.drawContours(image_color, [contour], -1, color[j], -1)

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'image_populated_contour' + image_name + '.png'
        ),
        image_color
    )

def calculateContourDistance(anchor_point, target_point):
    """ calculate the distance between two point """
    delta_x = target_point[0] - anchor_point[0]
    delta_y = target_point[1] - anchor_point[1]

    distance = math.sqrt(delta_x**2 + delta_y**2)
    distance = int(round(distance))

    return distance

def sortLeftToRightContours(contours):
    sorted_contours = imutils.contours.sort_contours(
        contours,
        method="left-to-right"
    )[0]

    return sorted_contours
