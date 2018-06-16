"""Save image"""
import cv2

def saveImage(path, image):
    """save image"""
    cv2.imwrite(path, image)
