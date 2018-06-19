""" find relative distance relative with first (LEFT TOP) skuk mark (black square box) """

import os
import math
import cv2
import imutils

def getSpecificSquarePoint(position, square_boxes):
    list_position = {'LT': 0, 'RT': 1, 'LB': 2, 'RB': 3}

    list_hipotenusa = list()
    list_index = list()

    index = 0
    for square_box in square_boxes:
        hipotenusa = int(
            math.sqrt(
                (square_box[0] * square_box[0]) + (square_box[1] * square_box[1])
            )
        )
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

def getRelativeAreaPoint(anchor_point, rectangles):
    relative_rectangles = []
    for rectangle in rectangles:
        deviation_1 = calculateDeviation(anchor_point, rectangle[0])
        deviation_2 = calculateDeviation(anchor_point, rectangle[1])
        section_name = rectangle[2]
        relative_rectangle = [deviation_1, deviation_2, section_name]
        relative_rectangles.append(relative_rectangle)

    return relative_rectangles

def getRealAreaPoint(anchor_point, relative_points):
    real_point = []
    for relative_point in relative_points:
        deviation_1 = calculateReverseDeviation(anchor_point, relative_point[0])
        deviation_2 = calculateReverseDeviation(anchor_point, relative_point[1])
        section_name = relative_point[2]
        relative_relative_point = [deviation_1, deviation_2, section_name]
        real_point.append(relative_relative_point)

    return real_point

def calculateReverseDeviation(point_1, point_2):
    x = point_2[0] + point_1[0]
    y = point_2[1] + point_1[1]

    return (x, y)

def calculateDeviation(point_1, point_2):
    dx = point_2[0] - point_1[0]
    dy = point_2[1] - point_1[1]

    return (dx, dy)

def calculateRelativePoint(square_boxes, area_points):
    left_top_square_box = getSpecificSquarePoint('LT', square_boxes)
    relative_area_points = getRelativeAreaPoint(left_top_square_box, area_points)

    return relative_area_points
