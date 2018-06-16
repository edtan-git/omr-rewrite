""" draw rectangle from array of points """

import os
import cv2
from omrRelativeDistance import getSpecificSquarePoint
from omrRelativeDistance import getRealAreaPoint

DIR_PROCESSING_RESULT = 'processing_result'
def drawRectangleFromRelativePoint(image, square_attributes, points):
    """ draw rectangle from relative point """
    left_top_square_box = getSpecificSquarePoint('LT', square_attributes)
    real_area_points = getRealAreaPoint(left_top_square_box, points)

    image = image.copy()
    # real_area_points = points
    for real_area_point in real_area_points:
        x_start = real_area_point[0][0]
        y_start = real_area_point[0][1]
        x_end = real_area_point[1][0]
        y_end = real_area_point[1][1]

        image = cv2.rectangle(image,
                              (x_start, y_start),
                              (x_end, y_end),
                              (139, 0, 139),
                              2
                             )

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'image_with_relative_point.png'
        ),
        image
    )
