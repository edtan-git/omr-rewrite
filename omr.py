""" rewrite omr code """

import os
import argparse
import cv2
import imutils
import numpy as np
import mysql.connector
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

def connectDatabase():
    tmp_data_con = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="omr_grader"
    )
    return tmp_data_con

def getMetaLik(data_conn, layout_name):
    cursor = data_conn.cursor()
    cursor.execute("SELECT * FROM meta_lik WHERE nama='" + layout_name + "'")

    result = cursor.fetchall()
    result = result[0]

    cursor.execute("SELECT * FROM meta_lik_detail WHERE id_meta_lik='" + result[1] + "'")

    meta_lik = []
    result_metas = cursor.fetchall()

    for result_meta in result_metas:
        meta_lik.append([
            (result_meta[3], result_meta[4]),
            (result_meta[5], result_meta[6]),
            result_meta[2]
        ])

    return meta_lik

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-i", "--image", required=True, help="Path to the input directory")
argument_parser.add_argument("-l", "--layout", required=True, help="layout name")

arguments = vars(argument_parser.parse_args())

layout_name = arguments['layout']
data_connection = connectDatabase()
meta_lik = getMetaLik(data_connection, layout_name)

relative_points = meta_lik

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

kernel = np.ones((2,2), np.uint8)
image_test_dilate = image_omr_sheet_thresh.copy()
dilation = cv2.dilate(image_test_dilate, kernel, iterations = 1)
path_gray = createPath(
    DIR_PROCESSING_RESULT,
    'IMAGE_DILATE-' + image_name + IMAGE_EXTENSION
)
saveImage(path_gray, dilation)

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

image_omr_sheet_thresh = dilation.copy()
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

# relative_points = [
#     [(-29, 481), (715, 1363), 'NAME'],
#     [(748, 511), (1196, 854), 'STUDENT_NUMBER'],
#     [(1231, 508), (1454, 850), 'DATE_OF_BIRTH'],
#     [(1378, 982), (1454, 1325), 'PACKAGE_NUMBER'],
#     [(4, 1415), (1429, 1813), 'ANSWER']
# ]

# 3 section 01
# relative_points = [
#     [(594, 924), (1345, 1818), 'NAME'],
#     [(76, 915), (541, 1269), 'STUDENT_NUMBER'],
#     [(-14, 399), (1432, 804), 'ANSWER']
# ]

# 3 section 02
# relative_points = [
#     [(591, 488), (1345, 1386), 'NAME'],
#     [(79, 486), (538, 841), 'STUDENT_NUMBER'],
#     [(-9, 1416), (1418, 1832), 'ANSWER']
# ]

# 4 section 03
# relative_points = [
#     [(596, 921), (1351, 1816), 'NAME'],
#     [(85, 916), (543, 1267), 'STUDENT_NUMBER'],
#     [(86, 1347), (316, 1699), 'DATE_OF_BIRTH'],
#     [(-11, 400), (1437, 808), 'ANSWER']
# ]

# 4 section 04
# relative_points = [
#     [(596, 479), (1349, 1370), 'NAME'],
#     [(86, 479), (538, 825), 'STUDENT_NUMBER'],
#     [(88, 951), (315, 1297), 'DATE_OF_BIRTH'],
#     [(-8, 1405), (1421, 1821), 'ANSWER']
# ]

# 5 section 05
# relative_points = [
#     [(600, 918), (1351, 1812), 'NAME'],
#     [(84, 952), (544, 1304), 'STUDENT_NUMBER'],
#     [(86, 1425), (318, 1777), 'DATE_OF_BIRTH'],
#     [(402, 1426), (485, 1774), 'PACKAGE_NUMBER'],
#     [(-1, 367), (1424, 762), 'ANSWER']
# ]

# 5 section 06
# relative_points = [
#     [(600, 918), (1351, 1812), 'NAME'],
#     [(81, 1423), (541, 1772), 'STUDENT_NUMBER'],
#     [(82, 943), (315, 1292), 'DATE_OF_BIRTH'],
#     [(400, 945), (480, 1288), 'PACKAGE_NUMBER'],
#     [(-1, 367), (1424, 762), 'ANSWER']
# ]

# 5 section 07
# relative_points = [
#     [(598, 481), (1349, 1370), 'NAME'],
#     [(88, 480), (538, 825), 'STUDENT_NUMBER'],
#     [(86, 951), (315, 1297), 'DATE_OF_BIRTH'],
#     [(404, 955), (484, 1302), 'PACKAGE_NUMBER'],
#     [(-8, 1405), (1421, 1821), 'ANSWER']
# ]
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
    rotated_threshold_image,
    {
        'image_name': image_name
    }
)
