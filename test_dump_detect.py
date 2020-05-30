import boto3
from cv2 import cv2 as cv
import json
import csv
import numpy as np

with open('C:/Users/alex5/Desktop/credentials.csv', 'r') as c:
    next(c)
    r = csv.reader(c)
    for l in r:
        kid = l[2]
        s_kid = l[3]

def detect_dump(img_path, last_img_path):
    sub = cv.createBackgroundSubtractorMOG2()
    curr = cv.imread(img_path)
    last = cv.imread(last_img_path)
    width = len(curr[0])
    height = len(curr)
    fgMask = sub.apply(last)
    fgMask = sub.apply(curr)
    kernel = np.ones((8,8), np.uint8)
    #dilation = cv.dilate(fgMask, kernel, iterations=1)
    
    thresh, bnw = cv.threshold(fgMask, 126, 255, cv.THRESH_BINARY)
   
    opening = cv.morphologyEx(bnw, cv.MORPH_OPEN, kernel)
    #closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, np.ones((10,10), np.uint8))
    cnts = cv.findContours(opening, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)[-2]
    max_area = 0
    if (len(cnts) > 0):
        for c in cnts:
            #approx = cv.approxPolyDP(c, 10, True)
            curr = cv.contourArea(c)
            max_area = max(max_area, curr)
    if max_area > width*height*0.8:
        print('maxarea', max_area)
        print(width*height*0.8)
        print('HE/SHE DID IT!!!!! REPORT!!!')
        #return True
    else:
        print('maxarea', max_area)
        print(width*height*0.8)
        print('No violation')
        #return False
    
    #---- TEST CODE -------------
    mask = np.zeros(opening.shape, np.uint8)
    sorted_cnts = sorted(cnts, key=cv.contourArea, reverse=True)
    cv.drawContours(mask, [sorted_cnts[0]], 0, 255, -1)
    #cv.drawContours(curr, c, -1, (0, 255, 0), 3)
    mask = cv.resize(mask, (600,400))
    cv.imshow('mask', mask)
    curr = cv.imread(img_path)
    cv.drawContours(curr, sorted_cnts, 0, (0, 255, 0), 3)
    curr = cv.resize(curr, (600, 400))
    cv.imshow('original', curr)
    cv.waitKey(0)
    cv.destroyAllWindows()
    ################################

def main():
    
    #format: top_STREETNAME_DATE for top camera
    #format2: in_STREETNAME_DATE for inner camera

    # get information from the stream filename

    video_path = "./test_footage/test_1.mp4"
    times = 0
    # street_name = cur_street

    frameFrequency = 10

    #####################################

    camera = cv.VideoCapture(video_path)
    while True:
        res, image = camera.read()
        times += 1
        if not res:
            print('not res , not image')
            break   
        if times%frameFrequency == 0:
            cv.imwrite("./test_footage/test_frames/" + str(times) + '.jpg', image)
            print('created1')
        print(times)
    print('end')
    camera.release()

#main()
curr = './test_footage/test_frames/680.jpg'
last = './test_footage/test_frames/660.jpg'
detect_dump(curr, last)