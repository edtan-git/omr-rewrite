""" flann based matcher testing """

import os
import numpy as np
import cv2
from matplotlib import pyplot as plt

DIR_QUERY_IMAGE = os.path.abspath("logo_example")
DIR_TRAIN_IMAGE = os.path.abspath("../sample/test-case/01/")
DIR_PROCESSING_RESULT = os.path.abspath("../processing_result/flann")

MIN_MATCH_COUNT = 50

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
        '001_normal.png'
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
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=100)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# Need to draw only good matches, so create a mask
# matchesMask = [[0, 0] for i in xrange(len(matches))]

# ratio test as per Lowe's paper
good = []
for i, (m, n) in enumerate(matches):
    if m.distance < 0.7 * n.distance:
        # matchesMask[i] = [1, 0]
        good.append(m)

if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    if not M is None:
        matchesMask = mask.ravel().tolist()

        h, w = image_query.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        image_train = cv2.polylines(image_train, [np.int32(dst)], True, 0, 3, cv2.LINE_AA)

        draw_params = dict(
            matchColor=(0, 255, 0), # draw matches in green color
            singlePointColor=None,
            matchesMask=matchesMask, # draw only inliers
            flags=2
        )

        image_fin = cv2.drawMatches(image_query, kp1, image_train, kp2, good, None, **draw_params)

        cv2.imwrite(
            os.path.join(
                DIR_PROCESSING_RESULT,
                'image_fin.png'
            ),
            image_fin
        )
    else:
        print "Not matches found..."
else:
    print "Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT)
    matchesMask = None
# plt.imshow(image_fin,),plt.show()
