""" rewrite omr code """

import os
import argparse
import cv2
import imutils
from omrUtilities import findBlackBoxAnchor
from omrUtilities import findDegreeBias
from omrUtilities import rotateImage
from drawRectangle import drawRectangleFromRelativePoint
from informationExtractor import findCircle
from informationExtractor import extractCircledBubble

IMAGE_EXTENSION = '.png'
DIR_PROCESSING_RESULT = 'processing_result'

def createPath(directory, filename):
    """create filename path"""
    path = os.path.join(directory, filename)
    return path

def saveImage(path, image):
    """save image to disk"""
    cv2.imwrite(path, image)

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-i", "--image", required=True, help="Path to the input directory")

arguments = vars(argument_parser.parse_args())

if not os.path.isdir(DIR_PROCESSING_RESULT):
    os.mkdir(DIR_PROCESSING_RESULT)

image_path = arguments['image']
image_path_list = image_path.split('/')

image_filename = image_path_list[len(image_path_list) - 1]
image_name_list = image_filename.split('.')

image_name = image_name_list[0]
image_extension = image_name_list[1]

image_omr_sheet = cv2.imread(image_path)
image_omr_sheet_gray = cv2.cvtColor(image_omr_sheet, cv2.COLOR_BGR2GRAY)
image_omr_sheet_blurred = cv2.GaussianBlur(image_omr_sheet_gray, (5, 5), 0)
image_omr_sheet_edged = cv2.Canny(image_omr_sheet_blurred, 100, 200)
image_omr_sheet_thresh = cv2.threshold(image_omr_sheet_gray, 0, 255,
                                       cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

path_gray = createPath(
    DIR_PROCESSING_RESULT,
    'IMAGE_OMR_SHEET_THRESHOLD-' + image_name + IMAGE_EXTENSION
)
saveImage(path_gray, image_omr_sheet_thresh)

image_omr_with_contour = image_omr_sheet.copy()
contours = cv2.findContours(image_omr_sheet_thresh, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if imutils.is_cv2() else contours[1]

index = 0
for contour in contours:
    point = (contour[0][0][0], contour[0][0][1])
    cv2.putText(image_omr_with_contour, str(index),
                point, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
    cv2.drawContours(image_omr_with_contour, [contour], -1, (0, 0, 255), 2)
    index = index + 1

path_gray = createPath(
    DIR_PROCESSING_RESULT,
    'IMAGE_OMR_SHEET_GRAY-' + image_name + IMAGE_EXTENSION
)
saveImage(path_gray, image_omr_sheet_gray)

path_blurred = createPath(
    DIR_PROCESSING_RESULT,
    'IMAGE_OMR_SHEET_BLURRED-' + image_name + IMAGE_EXTENSION
)
saveImage(path_blurred, image_omr_sheet_blurred)

path_edged = createPath(
    DIR_PROCESSING_RESULT,
    'IMAGE_OMR_SHEET_EDGED-' + image_name + IMAGE_EXTENSION
)
saveImage(path_edged, image_omr_sheet_edged)

path_w_contour = createPath(
    DIR_PROCESSING_RESULT,
    'IMAGE_OMR_SHEET_WITH_CONTOUR-' + image_name + IMAGE_EXTENSION
)
saveImage(path_w_contour, image_omr_with_contour)

#find black box anchor
options = {
    'image': image_omr_sheet,
    'image_edged': image_omr_sheet_edged,
    'image_threshold': image_omr_sheet_thresh,
    'image_name': image_name,
    'image_width': image_omr_sheet.shape[1]
}
return_black_box_anchor = findBlackBoxAnchor(contours, options)
ordered_square_boxes = return_black_box_anchor['ordered_square_contours']
square_attributes = return_black_box_anchor['square_attributes']
degree_bias = findDegreeBias(ordered_square_boxes)
rotated_image = rotateImage(image_omr_sheet,
                            degree_bias['rotation_matrix'],
                            {'image_name': image_name}
                           )
rotated_threshold_image = rotateImage(
    image_omr_sheet_thresh,
    degree_bias['rotation_matrix'],
    {'image_name': image_name + 'threshold'}
)
rotated_threshold_image = cv2.threshold(rotated_threshold_image, 0, 255,
                                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

rotated_edged_image = rotateImage(
    image_omr_sheet_edged,
    degree_bias['rotation_matrix'],
    {'image_name': image_name + 'edged'}
)
cv2.imwrite(
    os.path.join(
        DIR_PROCESSING_RESULT,
        'THRESHOLD_ROTATED_IMAGE_' + image_name + '.png'
    ),
    rotated_threshold_image
)

relative_points = [
    [(-29, 481), (715, 1363), 'NAME'],
    [(748, 511), (1196, 854), 'STUDENT_NUMBER'],
    [(1231, 508), (1454, 850), 'DATE_OF_BIRTH'],
    [(1378, 982), (1454, 1325), 'PACKAGE_NUMBER'],
    [(4, 1415), (1429, 1813), 'ANSWER']
]
drawRectangleFromRelativePoint(rotated_threshold_image, square_attributes, relative_points)

populated_contour = findCircle(
    rotated_threshold_image,
    {
        'image_name': image_name,
        'points': relative_points,
        'square_attributes': square_attributes
    }
)

extractCircledBubble(
    populated_contour,
    # cv2.cvtColor(rotated_threshold_image, cv2.COLOR_GRAY2RGB),
    rotated_threshold_image,
    {
        'image_name': image_name
    }
)
