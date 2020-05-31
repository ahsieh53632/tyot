import csv
import boto3
import json
import numpy as np
from cv2 import cv2 as cv
import os
from urllib.parse import unquote_plus
import uuid

with open('C:/Users/alex5/Desktop/credentials.csv', 'r') as c:
    next(c)
    r = csv.reader(c)
    for l in r:
        kid = l[2]
        s_kid = l[3]



def detect_dump(curr, last, f, cnt_img):
    sub = cv.createBackgroundSubtractorMOG2()
    width = len(curr[0])
    height = len(curr)
    fgMask = sub.apply(last)
    fgMask = sub.apply(curr, learningRate=0)
    kernel = np.ones((8,8), np.uint8)
    #dilation = cv.dilate(fgMask, kernel, iterations=1)
    thresh, bnw = cv.threshold(fgMask, 127, 255, cv.THRESH_BINARY)
    opening = cv.morphologyEx(bnw, cv.MORPH_OPEN, kernel)
    #closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, np.ones((10,10), np.uint8))

    cnts = cv.findContours(opening, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)[-2]
    max_area = 0
    sorted_cnts = sorted(cnts, key=cv.contourArea, reverse=True)
    cv.drawContours(cnt_img, sorted_cnts, 0, (0, 0, 255), 3)
    # find area in dump area
    if (len(sorted_cnts) > 0):
        mask = np.zeros(opening.shape, np.uint8)
        cv.drawContours(mask, [sorted_cnts[0]], 0, 255, -1) 
        crop_x_start = 500
        crop_x_end = 580
        crop_y_start = 670
        crop_y_end = 1300
        crop_size = (crop_y_end - crop_y_start) * (crop_x_end - crop_x_start) 
        croped = mask[crop_y_start:crop_y_end, crop_x_start:crop_x_end]
        area = 0
        for r in croped:
            for c in r:
                if c > 0:
                    area += 1

        if area > 0.3*crop_size:
            #cv.imwrite('./test_run/mask_' + str(f) + '.jpg', mask)
            #cv.imwrite('./test_run/crop_' + str(f) + '.jpg', croped)
            return True
        else:
            return False
    
    else:
        #print('contours not found')
        return False



    
    # #---- TEST CODE -------------
    # cv.imshow('foreground', opening)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    # ################################

def main(view):
    #format: STREETNAME_DATE for top camera
    #format2: STREETNAME_DATE for inner camera

    # get information from the stream filename
    items = view.split('_')
    street_name = items[0]
    date = items[1]

    times = 0
    frameFrequency = 10
    #####################################
    camera = cv.VideoCapture(view)
    res, frame = camera.read()
    if not res:
        print('can not read frame')
        return 
    last = frame
    last_face = frame
    pause = 0

    # skip one frame
    res, frame = camera.read()
    if not res:
        print('can not read frame')
        return 
    while True:
        res, frame = camera.read()
        times += 1
        if not res:
            # print('not res , not image')
            break   
        if times%frameFrequency == 0:
            print('detecting violation at frame' + str(times))
            if (pause > 0):
                pause -= 1
            else:
                cnt_img = frame.copy()
                result = detect_dump(frame, last, times, cnt_img)
                if (result):
                    print('######################################')
                    print(' found violation at frame' + str(times))
                    print('######################################')
                    p_name = 'person_' + str(times) + '.jpg'
                    p_path = "./test_run/" + p_name
                    obj_name = 'obj_' + str(times) + '.jpg'
                    obj_path = "./test_run/" + obj_name
                    cv.imwrite(p_path, last_face)
                    cv.imwrite(obj_path, cnt_img)
                    # skip 2 frames to avoid redundant searches
                    pause = 4
        if times%(frameFrequency*1.5) == 0:
            last_face = frame
    camera.release()


# guaranted that both video exsists in S3 bucket
main('./test_footage/中央路_20200532.mp4')