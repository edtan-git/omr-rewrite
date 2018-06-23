""" collection of extractor type """
import os
import datetime
import cv2
import numpy as np
import imutils

DIR_PROCESSING_RESULT = 'processing_result'

def extractName(contours, image_threshold):
    """ extract information from vertical aligned bubble """
    print 'extractName was called'
    color = [
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (255, 255, 0),
        (255, 0, 255)
    ]
    DATA_SORT = 'HORIZONTAL'
    DATA_LENGTH = 20
    DATA_OPTIONS_LENGTH = 26
    log_result_content = ''

    file_name = createSelectedItemLogFileName()
    file = open(file_name, 'w+')

    # image_threshold_color = cv2.cvtColor(image_threshold.copy(), cv2.COLOR_GRAY2RGB)
    image_threshold_color = image_threshold.copy()

    index = 0
    for (q, i) in enumerate(np.arange(0, len(contours), DATA_OPTIONS_LENGTH)):
        tmp_contours = imutils.contours.sort_contours(
            contours[i:i+DATA_OPTIONS_LENGTH],
            method="top-to-bottom"
        )[0]

        for (j, contour) in enumerate(tmp_contours):
            index += 1
            (x, y, w, h) = cv2.boundingRect(contour)
            image_threshold_color = cv2.putText(
                image_threshold_color,
                str(index),
                (x, y),
                cv2.FONT_HERSHEY_COMPLEX,
                0.5,
                (0, 255, 0),
                1
            )
            image_threshold_color = cv2.drawContours(
                image_threshold_color,
                [contour],
                -1,
                color[q%5],
                -1
            )
    
    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'SELECTED_OPTIONS.png'
        ),
        image_threshold_color
    )

    return image_threshold_color

def extractStudentNumber(contours, image_threshold):
    print 'extractStudentNumber was called'
    color = [
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (255, 255, 0),
        (255, 0, 255)
    ]
    DATA_SORT = 'HORIZONTAL'
    DATA_LENGTH = 20
    DATA_OPTIONS_LENGTH = 10
    log_result_content = ''

    file_name = createSelectedItemLogFileName()
    file = open(file_name, 'w+')

    # image_threshold_color = cv2.cvtColor(image_threshold.copy(), cv2.COLOR_GRAY2RGB)
    image_threshold_color = image_threshold.copy()

    index = 0
    for (q, i) in enumerate(np.arange(0, len(contours), DATA_OPTIONS_LENGTH)):
        tmp_contours = imutils.contours.sort_contours(
            contours[i:i+DATA_OPTIONS_LENGTH],
            method="top-to-bottom"
        )[0]

        for (j, contour) in enumerate(tmp_contours):
            index += 1
            (x, y, w, h) = cv2.boundingRect(contour)
            image_threshold_color = cv2.putText(
                image_threshold_color,
                str(index),
                (x, y),
                cv2.FONT_HERSHEY_COMPLEX,
                0.5,
                (0, 255, 0),
                1
            )
            image_threshold_color = cv2.drawContours(
                image_threshold_color,
                [contour],
                -1,
                color[q%5],
                -1
            )

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'SELECTED_OPTIONS.png'
        ),
        image_threshold_color
    )
    return image_threshold_color

def extractDateOfBirth(contours, image_threshold):
    """ extract information from vertical aligned bubble """
    print 'extractDateOfBirth was called'
    color = [
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (255, 255, 0),
        (255, 0, 255)
    ]
    DATA_SORT = 'HORIZONTAL'
    DATA_LENGTH = 20
    DATA_OPTIONS_LENGTHS = [4, 10, 2, 10, 10, 10]
    # DATA_OPTIONS_LENGTH = 8
    log_result_content = ''

    file_name = createSelectedItemLogFileName()
    file = open(file_name, 'w+')

    # image_threshold_color = cv2.cvtColor(image_threshold.copy(), cv2.COLOR_GRAY2RGB)
    image_threshold_color = image_threshold.copy()

    start = 0
    index = 0
    color_counter = 0
    for data_options_length in DATA_OPTIONS_LENGTHS:
        color_counter += 1
        end = start + data_options_length
        process_contours = contours[start:end]
        start = end

        tmp_contours = imutils.contours.sort_contours(
            process_contours,
            method="top-to-bottom"
        )[0]

        for (j, contour) in enumerate(tmp_contours):
            index += 1
            (x, y, w, h) = cv2.boundingRect(contour)
            image_threshold_color = cv2.putText(
                image_threshold_color,
                str(index),
                (x, y),
                cv2.FONT_HERSHEY_COMPLEX,
                0.5,
                (0, 255, 0),
                1
            )
            image_threshold_color = cv2.drawContours(
                image_threshold_color,
                [contour],
                -1,
                color[color_counter%5],
                -1
            )

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'SELECTED_OPTIONS.png'
        ),
        image_threshold_color
    )

    return image_threshold_color

def extractPackageNumber(contours, image_threshold):
    """ extract package number """
    print 'extractPackageNumber was called'
    color = [
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (255, 255, 0),
        (255, 0, 255)
    ]
    DATA_SORT = 'HORIZONTAL'
    DATA_LENGTH = 20
    DATA_OPTIONS_LENGTH = 10
    log_result_content = ''

    file_name = createSelectedItemLogFileName()
    file = open(file_name, 'w+')

    # image_threshold_color = cv2.cvtColor(image_threshold.copy(), cv2.COLOR_GRAY2RGB)
    image_threshold_color = image_threshold.copy()

    index = 0
    for (q, i) in enumerate(np.arange(0, len(contours), DATA_OPTIONS_LENGTH)):
        tmp_contours = imutils.contours.sort_contours(
            contours[i:i+DATA_OPTIONS_LENGTH],
            method="top-to-bottom"
        )[0]

        for (j, contour) in enumerate(tmp_contours):
            index += 1
            (x, y, w, h) = cv2.boundingRect(contour)
            image_threshold_color = cv2.putText(
                image_threshold_color,
                str(index),
                (x, y),
                cv2.FONT_HERSHEY_COMPLEX,
                0.5,
                (0, 255, 0),
                1
            )
            image_threshold_color = cv2.drawContours(
                image_threshold_color,
                [contour],
                -1,
                color[q%5],
                -1
            )

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'SELECTED_OPTIONS.png'
        ),
        image_threshold_color
    )

    return image_threshold_color

def extractAnswerSheet(contours, image_threshold):
    """ extract answer sheet """
    print "extractAnswerSheet was called"
    color = [
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (255, 255, 0),
        (255, 0, 255)
    ]
    DATA_SORT = 'HORIZONTAL'
    DATA_LENGTH = 5
    DATA_OPTIONS_LENGTH = 50
    log_result_content = ''

    file_name = createSelectedItemLogFileName()
    file = open(file_name, 'w+')

    # image_threshold_color = cv2.cvtColor(image_threshold.copy(), cv2.COLOR_GRAY2RGB)
    image_threshold_color = image_threshold.copy()

    contours = imutils.contours.sort_contours(
        contours,
        method="left-to-right"
    )[0]

    index = 0
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

            for contour in tmp_answer_contours:
                index += 1
                (x, y, w, h) = cv2.boundingRect(contour)
                image_threshold_color = cv2.putText(
                    image_threshold_color,
                    str(index),
                    (x, y),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.5,
                    (0, 255, 0),
                    1
                )
                image_threshold_color = cv2.drawContours(
                    image_threshold_color,
                    [contour],
                    -1,
                    color[r%5],
                    -1
                )

        # for contour in tmp_contours:
        #     index += 1
        #     (x, y, w, h) = cv2.boundingRect(contour)
        #     image_threshold_color = cv2.putText(
        #         image_threshold_color,
        #         str(index),
        #         (x, y),
        #         cv2.FONT_HERSHEY_COMPLEX,
        #         0.5,
        #         (0, 255, 0),
        #         1
        #     )
        #     image_threshold_color = cv2.drawContours(
        #         image_threshold_color,
        #         [contour],
        #         -1,
        #         color[q%5],
        #         -1
        #     )

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'SELECTED_OPTIONS_ANSWER.png'
        ),
        image_threshold_color
    )

    return image_threshold_color

    index = 0
    for (q, i) in enumerate(np.arange(0, len(contours), DATA_OPTIONS_LENGTH)):
        tmp_contours = imutils.contours.sort_contours(
            contours[i:i+DATA_OPTIONS_LENGTH],
            method="left-to-right"
        )[0]

        for (j, contour) in enumerate(tmp_contours):
            index += 1
            (x, y, w, h) = cv2.boundingRect(contour)
            image_threshold_color = cv2.putText(
                image_threshold_color,
                str(index),
                (x, y),
                cv2.FONT_HERSHEY_COMPLEX,
                0.5,
                (0, 255, 0),
                1
            )
            image_threshold_color = cv2.drawContours(
                image_threshold_color,
                [contour],
                -1,
                color[q%5],
                -1
            )

    cv2.imwrite(
        os.path.join(
            DIR_PROCESSING_RESULT,
            'SELECTED_OPTIONS.png'
        ),
        image_threshold_color
    )

    return image_threshold_color

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
