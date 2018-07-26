""" get distance in (x, y) from an area point relatively to square box LT """

import os
import cv2
import imutils
import math

def getSquarePoint(position, square_boxes):
    list_position = {'LT': 0, 'RT': 1, 'LB': 2, 'RB': 3}

    list_hipotenusa = list()
    list_index = list()

    index = 0
    for square_box in square_boxes:
        hipotenusa = int(math.sqrt((square_box[0] * square_box[0])
                                   + (square_box[1] * square_box[1])))
        list_hipotenusa.append(hipotenusa)
        list_index.append(index)

    list_hipotenusa_sorted = sorted(list_hipotenusa)
    target_hipotenusa = list_hipotenusa_sorted[list_position[position]]

    index = 0
    for hipotenusa in list_hipotenusa:
        if hipotenusa == target_hipotenusa:
            break
        index = index + 1

    return (square_boxes[index][0], square_boxes[index][1])


def getSquareBox(omr_image):
    # define square box criteria
    ratio = omr_image.shape[1] / float(1700)
    ar_min = 0.958
    ar_max = 1.28
    w_min = 31 * ratio
    w_max = 36 * ratio
    h_min = 28 * ratio
    h_max = 33 * ratio

    square_boxes_cnts = list()
    square_boxes = list()

    omr_image_gray = cv2.cvtColor(omr_image, cv2.COLOR_BGR2GRAY)
    omr_image_blurred = cv2.GaussianBlur(omr_image_gray, (5, 5), 0)
    omr_image_edged = cv2.Canny(omr_image_blurred, 75, 200)

    cnts = cv2.findContours(omr_image_edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # filter which contours is the square box
    for contour in cnts:
        (x, y, w, h) = cv2.boundingRect(contour)
        if h == 0 or w == 0:
            continue

        ar = w / float(h)
        is_ar_criteria_pass = ar >= ar_min and ar <= ar_max
        is_w_criteria_pass = w >= w_min and w <= w_max
        is_h_criteria_pass = h >= h_min and h <= h_max

        if is_ar_criteria_pass and is_w_criteria_pass and is_h_criteria_pass:
            square_boxes_cnts.append(contour)
            square_boxes.append((x, y, w, h))

    return square_boxes

def getRelativeAreaPoint(anchor_point, rectangles):
    relative_rectangles = []
    for rectangle in rectangles:
        deviation_1 = calculateDeviation(anchor_point, rectangle[0])
        deviation_2 = calculateDeviation(anchor_point, rectangle[1])
        relative_rectangle = [deviation_1, deviation_2]
        relative_rectangles.append(relative_rectangle)

    return relative_rectangles

def calculateDeviation(point_1, point_2):
    dx = point_2[0] - point_1[0]
    dy = point_2[1] - point_1[1]

    return (dx, dy)

def drawRectangle(rectangles, image):
    for rectangle in rectangles:
        for rectangle_point in rectangle:
            cv2.circle(image, (rectangle_point), 10, (255, 0, 0), -1)

    cv2.imwrite('testing.png', image)

# area points
# rectangles = [
#     [(116, 546), (880, 1455)], # nama
#     [(896, 586), (1346, 940)], # nomor peserta
#     [(1376, 586), (1606, 943)], # tanggal lahir
#     [(1523, 1066), (1606, 1427)], # paket soal
#     [(906, 1083), (1480, 1227)], # kelompok belajar
#     [(150, 1543), (1570, 1950)] # jawaban
# ]
# rectangles = [
#     [(126, 562), (860, 1447)],  # NAMA
#     [(904, 596), (970, 934)],  # NOMOR PESERTA PART 1
#     [(1013, 594), (1120, 933)],  # NOMOR PESERTA PART 2
#     [(1162, 595), (1266, 934)],  # NOMOR PESERTA PART 3
#     [(1309, 594), (1341, 934)]  # NOMOR PESERTA PART 4
# ]
# 3 section 01
# rectangles = [
#     [(751, 1033), (1502, 1927)], # NAMA
#     [(233, 1024), (698, 1378)], # NOMOR SISWA
#     [(143, 508), (1589, 913)], # JAWABAN
# ]

# 3 section 02
# rectangles = [
#     [(748, 597), (1502, 1495)], # NAMA
#     [(236, 595), (695, 950)], # NOMOR SISWA
#     [(148, 1525), (1575, 1941)], # JAWABAN
# ]

# 4 section 01
# rectangles = [
#     [(747, 1036), (1502, 1931)], # NAMA
#     [(236, 1031), (694, 1382)], # NOMOR SISWA
#     [(237, 1462), (467, 1814)], # TANGGAL LAHIR
#     [(140, 515), (1588, 923)], # JAWABAN
# ]

# 4 section 02
# rectangles = [
#     [(747, 594), (1500, 1485)], # NAMA
#     [(237, 594), (689, 940)], # NOMOR SISWA
#     [(239, 1066), (466, 1412)], # TANGGAL LAHIR
#     [(143, 1520), (1572, 1936)], # JAWABAN
# ]

# 5 section 01
# rectangles = [
#     [(751, 1033), (1502, 1927)], # NAMA
#     [(235, 1067), (695, 1419)], # NOMOR SISWA
#     [(237, 1540), (469, 1892)], # TANGGAL LAHIR
#     [(553, 1541), (636, 1889)], # PAKET SOAL
#     [(150, 482), (1575, 877)], # JAWABAN
# ]

# 5 section 03
rectangles = [
    [(749, 596), (1500, 1485)], # NAMA
    [(239, 595), (689, 940)], # NOMOR SISWA
    [(237, 1066), (466, 1412)], # TANGGAL LAHIR
    [(555, 1070), (635, 1417)], # PAKET SOAL
    [(143, 1520), (1572, 1936)], # JAWABAN
]


dir_name = "sample/4-section"
# image_name = "after_rotation.png"
image_name = "01_011_4_section_normal_1.png"

image = os.path.join(dir_name, image_name)
image_omr_sheet = cv2.imread(image)

square_boxes = getSquareBox(image_omr_sheet)
tuple_square_boxes = getSquarePoint("LT", square_boxes)
drawRectangle(rectangles, image_omr_sheet)
relative_rectangles = getRelativeAreaPoint(tuple_square_boxes, rectangles)

print relative_rectangles

# cv2.circle(image_omr_sheet, tuple_square_boxes, 0, (0, 255, 0), 0)
# cv2.imwrite('image_omr_sheet.png', image_omr_sheet)

# cv2.imshow("image", image_omr_sheet)
# cv2.waitKey(0)
