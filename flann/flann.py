""" flann based matcher testing """

import os
import numpy as np
import cv2
from matplotlib import pyplot as plt

DIR_QUERY_IMAGE = os.path.abspath("logo_example")
DIR_TRAIN_IMAGE = os.path.abspath("../sample/sample-w-logo")
DIR_PROCESSING_RESULT = os.path.abspath("../processing_result")

print DIR_QUERY_IMAGE
print DIR_TRAIN_IMAGE
print DIR_PROCESSING_RESULT

image_query = cv2.imread(
    os.path.join(
        DIR_QUERY_IMAGE,
        'logo-dikti-bg-white.png'
    ),
    0
)

image_train = cv2.imread(
    os.path.join(
        DIR_TRAIN_IMAGE,
        'ristek.png'
    ),
    0
)

cv2.imwrite(
    os.path.join(
        DIR_PROCESSING_RESULT,
        'image_train.png'
    ),
    image_train
)

cv2.imwrite(
    os.path.join(
        DIR_PROCESSING_RESULT,
        'image_query.png'
    ),
    image_query
)

sift = cv2.xfeatures2d.SIFT_create()

# find key point and descriptor
kp1, des1 = sift.detectAndCompute(image_query, None)
kp2, des2 = sift.detectAndCompute(image_train, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0, 0] for i in xrange(len(matches))]

# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    if m.distance < 0.7 * n.distance:
        matchesMask[i] = [1, 0]

draw_params = dict(
    matchColor=(0, 255, 0),
    singlePointColor=(255, 0, 0),
    matchesMask=matchesMask,
    flags=0
)

image_fin = cv2.drawMatchesKnn(image_query, kp1, image_train, kp2, matches, None, **draw_params)

cv2.imwrite(
    os.path.join(
        DIR_PROCESSING_RESULT,
        'image_fin.png'
    ),
    image_fin
)
# plt.imshow(image_fin,),plt.show()
