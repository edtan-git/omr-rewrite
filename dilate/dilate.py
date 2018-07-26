import cv2 
import numpy as np

image = cv2.imread("image.png")

cv2.imshow('Original', image)
cv2.waitKey(0)

kernel = np.ones((5,5), np.uint8)

dilation = cv2.dilate(image, kernel, iterations = 3)
cv2.imshow('Dilation', dilation)
cv2.waitKey(0)

closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
cv2.imshow('Closing', closing)
cv2.waitKey(0)