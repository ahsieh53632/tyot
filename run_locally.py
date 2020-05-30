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



def detect_dump(curr, last):
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

    cv.drawContours(opening, sorted_cnts, 0, (128, 128, 128), 3)
    if (len(cnts) > 0):
        for c in cnts:
            curr = cv.contourArea(c)
            max_area = max(max_area, curr)
    if max_area > width*height*0.8:
        #print('maxarea', max_area)
        #print('HE/SHE DID IT!!!!! REPORT!!!')
        return True
    else:
        #print('maxarea', max_area)
        #print('No violation')
        return False
    
    # #---- TEST CODE -------------
    # cv.imshow('foreground', opening)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    # ################################

def main(top_view, in_view):
    #format: top_STREETNAME_DATE for top camera
    #format2: in_STREETNAME_DATE for inner camera

    # get information from the stream filename
    items = top_view.split('_')
    street_name = items[1]
    date = items[2]

    times = 0
    frameFrequency = 10
    #####################################
    camera_top_view = cv.VideoCapture(top_view)
    camera_in_view = cv.VideoCapture(in_view)
    res_top_view, frame_top_view = camera_top_view.read()
    res_in_view, frame_in_view = camera_in_view.read()

    if not (res_in_view and res_top_view):
        print('either one is missing one frame')
        return 
    last = frame_in_view
    pause = 0
    while True:
        res_top_view, frame_top_view = camera_top_view.read()
        res_in_view, frame_in_view = camera_in_view.read()
        times += 1
        if not (res_top_view and res_in_view):
            # print('not res , not image')
            break   
        if times%frameFrequency == 0:
            print('detecting violation at frame' + str(times))
            if (pause > 0):
                pause -= 1
            else:
                if (detect_dump(frame_in_view, last)):
                    print('######################################')
                    print(' found violation at frame' + str(times))
                    print('######################################')
                    obj_name = 'obj_' + str(uuid.uuid4()) + '.jpg'
                    p_name = 'person_' + str(uuid.uuid4()) + '.jpg'
                    obj_path = "./test_run/" +  obj_name
                    p_path = "./test_run/" + p_name
                    cv.imwrite(obj_path, frame_in_view)
                    cv.imwrite(p_path, frame_top_view)
                    # skip 2 frames to avoid redundant searches
                    pause = 2
    camera_top_view.release()
    camera_in_view.release()



# guaranted that both video exsists in S3 bucket
main('./test_footage/test_1.mp4', './test_footage/test_1.mp4')