""" sort populated contours """

import cv2

def sortPopulatedContours(populated_contours, image):
    """ sort populated contours """
    print "sortPopulatedContours called"
    print image.shape
    sorted_populated_contours = {}

    for index_name in populated_contours:
        populated_contour = populated_contours[index_name]
        contours = populated_contour['contours']
        contour_distances = populated_contour['contour_distances']

        sorted_contours = sorted(
            contours,
            key=lambda contour: cv2.boundingRect(contour)[0]
        )

        

        sorted_populated_contours[index_name] = {}
        sorted_populated_contours[index_name]['contours'] = sorted_contours

    return sorted_populated_contours
