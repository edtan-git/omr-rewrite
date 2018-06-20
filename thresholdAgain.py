import os
import cv2

DIR_PROCESSING_RESULT = 'processing_result_rethresholding'

def createPath(directory, filename):
    """create filename path"""
    path = os.path.join(directory, filename)
    return path

def saveImage(path, image):
    """save image to disk"""
    cv2.imwrite(path, image)

image_path = 'processing_result/threshold-image/threshold again.png'
image_omr_sheet = cv2.imread(image_path)

image_omr_sheet_gray = cv2.cvtColor(image_omr_sheet, cv2.COLOR_BGR2GRAY)
image_omr_sheet_blurred = cv2.GaussianBlur(image_omr_sheet_gray, (5, 5), 0)
image_omr_sheet_edged = cv2.Canny(image_omr_sheet_blurred, 100, 200)
image_omr_sheet_thresh = cv2.threshold(image_omr_sheet_gray, 0, 255,
                                       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

path_gray = createPath(
    DIR_PROCESSING_RESULT,
    'RETHRESHOLDIND.png'
)
saveImage(path_gray, image_omr_sheet_thresh)