""" collection of extractor type """
import os
import datetime
import cv2
import numpy as np
import imutils

DIR_PROCESSING_RESULT = 'processing_result'
BASE_OPTIONS_ALPHABET = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]
BASE_OPTIONS_NUMBER = [
    '1', '2', '3', '4', '5',
    '6', '7', '8', '9', '0'
]
COLOR = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (255, 0, 255)
]

def extractName(contours, image_threshold):
    """ extract information from vertical aligned bubble """
    print 'extractName was called'
    DATA_OPTIONS_LENGTH = 26

    # image_threshold_color = cv2.cvtColor(image_threshold.copy(), cv2.COLOR_GRAY2RGB)
    image_threshold_color = image_threshold.copy()
    image_threshold = cv2.cvtColor(image_threshold, cv2.COLOR_BGR2GRAY)

    selected_options = list()
    for (q, i) in enumerate(np.arange(0, len(contours), DATA_OPTIONS_LENGTH)):
        tmp_contours = imutils.contours.sort_contours(
            contours[i:i+DATA_OPTIONS_LENGTH],
            method="top-to-bottom"
        )[0]

        selected_options.append(list())
        tmp_selected_values = list()
        tmp_selected_values.append(None)
        for (j, contour) in enumerate(tmp_contours):
            return_check_contour = checkIfContourSelected(
                image_threshold,
                image_threshold_color,
                contour,
                selected_options,
                {
                    'index_contour': j,
                    'tmp_selected_values': tmp_selected_values
                }
            )

            tmp_selected_values = return_check_contour['tmp_selected_values']
            image_threshold_color = return_check_contour['image_threshold_color']

        selected_options[len(selected_options) - 1] = tmp_selected_values

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'SELECTED_OPTIONS.png'
        ),
        image_threshold_color
    )

    print selected_options

    return image_threshold_color

def extractStudentNumber(contours, image_threshold):
    """ extract student number """
    print 'extractStudentNumber was called'
    DATA_OPTIONS_LENGTH = 10

    # image_threshold_color = cv2.cvtColor(image_threshold.copy(), cv2.COLOR_GRAY2RGB)
    image_threshold_color = image_threshold.copy()
    image_threshold = cv2.cvtColor(image_threshold, cv2.COLOR_BGR2GRAY)

    selected_options = list()
    for (q, i) in enumerate(np.arange(0, len(contours), DATA_OPTIONS_LENGTH)):
        tmp_contours = imutils.contours.sort_contours(
            contours[i:i+DATA_OPTIONS_LENGTH],
            method="top-to-bottom"
        )[0]

        selected_options.append(list())
        tmp_selected_values = list()
        tmp_selected_values.append(None)
        for (j, contour) in enumerate(tmp_contours):
            return_check_contour = checkIfContourSelected(
                image_threshold,
                image_threshold_color,
                contour,
                selected_options,
                {
                    'index_contour': j,
                    'tmp_selected_values': tmp_selected_values
                }
            )

            tmp_selected_values = return_check_contour['tmp_selected_values']
            image_threshold_color = return_check_contour['image_threshold_color']

        selected_options[len(selected_options) - 1] = tmp_selected_values

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'SELECTED_OPTIONS.png'
        ),
        image_threshold_color
    )

    print selected_options

    return image_threshold_color

def extractDateOfBirth(contours, image_threshold):
    """ extract information from vertical aligned bubble """
    print 'extractDateOfBirth was called'

    DATA_OPTIONS_LENGTHS = [4, 10, 2, 10, 10, 10]

    # image_threshold_color = cv2.cvtColor(image_threshold.copy(), cv2.COLOR_GRAY2RGB)
    image_threshold_color = image_threshold.copy()
    image_threshold = cv2.cvtColor(image_threshold, cv2.COLOR_BGR2GRAY)

    start = 0
    selected_options = list()
    for data_options_length in DATA_OPTIONS_LENGTHS:
        end = start + data_options_length
        process_contours = contours[start:end]
        start = end

        tmp_contours = imutils.contours.sort_contours(
            process_contours,
            method="top-to-bottom"
        )[0]

        selected_options.append(list())
        tmp_selected_values = list()
        tmp_selected_values.append(None)
        for (j, contour) in enumerate(tmp_contours):
            return_check_contour = checkIfContourSelected(
                image_threshold,
                image_threshold_color,
                contour,
                selected_options,
                {
                    'index_contour': j,
                    'tmp_selected_values': tmp_selected_values
                }
            )

            tmp_selected_values = return_check_contour['tmp_selected_values']
            image_threshold_color = return_check_contour['image_threshold_color']

        selected_options[len(selected_options) - 1] = tmp_selected_values

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'SELECTED_OPTIONS.png'
        ),
        image_threshold_color
    )

    print selected_options

    return image_threshold_color

def extractPackageNumber(contours, image_threshold):
    """ extract package number """
    print 'extractPackageNumber was called'
    DATA_OPTIONS_LENGTH = 10

    # image_threshold_color = cv2.cvtColor(image_threshold.copy(), cv2.COLOR_GRAY2RGB)
    image_threshold_color = image_threshold.copy()
    image_threshold = cv2.cvtColor(image_threshold, cv2.COLOR_BGR2GRAY)

    selected_options = list()
    for (q, i) in enumerate(np.arange(0, len(contours), DATA_OPTIONS_LENGTH)):
        tmp_contours = imutils.contours.sort_contours(
            contours[i:i+DATA_OPTIONS_LENGTH],
            method="top-to-bottom"
        )[0]

        selected_options.append(list())
        tmp_selected_values = list()
        tmp_selected_values.append(None)
        for (j, contour) in enumerate(tmp_contours):
            return_check_contour = checkIfContourSelected(
                image_threshold,
                image_threshold_color,
                contour,
                selected_options,
                {
                    'index_contour': j,
                    'tmp_selected_values': tmp_selected_values
                }
            )

            tmp_selected_values = return_check_contour['tmp_selected_values']
            image_threshold_color = return_check_contour['image_threshold_color']

        selected_options[len(selected_options) - 1] = tmp_selected_values

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'SELECTED_OPTIONS.png'
        ),
        image_threshold_color
    )

    print selected_options

    return image_threshold_color

def extractAnswerSheet(contours, image_threshold):
    """ extract answer sheet """
    print "extractAnswerSheet was called"
    DATA_LENGTH = 5
    DATA_OPTIONS_LENGTH = 50

    # image_threshold_color = cv2.cvtColor(image_threshold.copy(), cv2.COLOR_GRAY2RGB)
    image_threshold_color = image_threshold.copy()
    image_threshold = cv2.cvtColor(image_threshold.copy(), cv2.COLOR_BGR2GRAY)

    contours = imutils.contours.sort_contours(
        contours,
        method="left-to-right"
    )[0]

    selected_options = list()
    tmp_result = list()
    for (q, i) in enumerate(np.arange(0, len(contours), DATA_OPTIONS_LENGTH)):
        tmp_contours = imutils.contours.sort_contours(
            contours[i:i+DATA_OPTIONS_LENGTH],
            method="top-to-bottom"
        )[0]

        for (r, j) in enumerate(np.arange(0, len(tmp_contours), DATA_LENGTH)):
            tmp_answer_contours = imutils.contours.sort_contours(
                tmp_contours[j:j+DATA_LENGTH],
                method="left-to-right"
            )[0]

            selected_options.append(list())
            tmp_selected_values = list()
            tmp_selected_values.append(None)
            for (s, contour) in enumerate(tmp_answer_contours):
                return_check_contour = checkIfContourSelected(
                    image_threshold,
                    image_threshold_color,
                    contour,
                    selected_options,
                    {
                        'index_contour': s,
                        'tmp_selected_values': tmp_selected_values
                    }
                )

                tmp_selected_values = return_check_contour['tmp_selected_values']
                image_threshold_color = return_check_contour['image_threshold_color']

            selected_options[len(selected_options) - 1] = tmp_selected_values

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'SELECTED_OPTIONS_ANSWER.png'
        ),
        image_threshold_color
    )

    print selected_options

    return image_threshold_color

def checkIfContourSelected(image_threshold, image_threshold_color, contour, selected_options, options):
    selected = False
    index_contour = options['index_contour']
    tmp_selected_values = options['tmp_selected_values']
    value_type = 'ALPHABET'
    if 'value_type' in options:
        value_type = 'NUMERIC'

    (x, y, w, h) = cv2.boundingRect(contour)

    mask = np.zeros(image_threshold.shape, dtype="uint8")
    cv2.drawContours(mask, [contour], -1, 255, -1)

    mask = cv2.bitwise_and(image_threshold, image_threshold, mask=mask)
    total = cv2.countNonZero(mask)
    total_area = cv2.contourArea(contour)

    percentage_covered = total / total_area

    if percentage_covered > 0.9:
        selected = True

        image_threshold_color = cv2.putText(
            image_threshold_color,
            str(index_contour),
            (x, y),
            cv2.FONT_HERSHEY_COMPLEX,
            0.5,
            (0, 0, 255),
            1
        )
        image_threshold_color = cv2.drawContours(
            image_threshold_color,
            [contour],
            -1,
            (0, 255, 0),
            -1
        )

    selected_value = None
    if selected:
        selected_value = index_contour

    if selected_value != None:
        if tmp_selected_values[0] is None:
            tmp_selected_values = list()
            tmp_selected_values.append(selected_value)
        else:
            tmp_selected_values.append(selected_value)

    return {
        'selected_value': selected_value,
        'selected_options': selected_options,
        'image_threshold_color': image_threshold_color,
        'tmp_selected_values': tmp_selected_values
    }

def getSelectedValue(value_type, index):
    """ return value from selected index """
    if value_type == 'ALPHABET':
        return_value = ' '
        if index in BASE_OPTIONS_ALPHABET:
            return_value = BASE_OPTIONS_ALPHABET[index]

        return return_value
    elif value_type == 'NUMERIC':
        return BASE_OPTIONS_NUMBER[index]

def createSelectedItemLogFileName():
    """ create selected item log filename """
    now_datetime = datetime.datetime.now()
    formated_datetime = str(now_datetime.year) + '{:02d}'.format(now_datetime.month)
    formated_datetime += '{:02d}'.format(now_datetime.day) + '{:02d}'.format(now_datetime.day)
    formated_datetime += '{:02d}'.format(now_datetime.hour) + '{:02d}'.format(now_datetime.minute)
    formated_datetime += '{:02d}'.format(now_datetime.second)
    file_name = 'extract_information_result/' + formated_datetime + '.txt'

    return file_name

def createSelectedItemLogContent(index, percentage_covered):
    log_result_content = "this is selected "
    log_result_content += str(index) + " "
    log_result_content += str(percentage_covered) + " "
    log_result_content += "\n"

    return log_result_content
