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
    fgMask = sub.apply(curr, learningRate=0)
    kernel = np.ones((5,5), np.uint8)
    #dilation = cv.dilate(fgMask, kernel, iterations=1)
    thresh, bnw = cv.threshold(fgMask, 127, 255, cv.THRESH_BINARY)
    opening = cv.morphologyEx(bnw, cv.MORPH_OPEN, kernel)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, np.ones((10,10), np.uint8))
    cnts = cv.findContours(closing, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)[-2]
    max_area = 0
    if (len(cnts) > 0):
        for c in cnts:
            #approx = cv.approxPolyDP(c, 10, True)
            curr = cv.contourArea(c)
            max_area = max(max_area, curr)
    if max_area > width*height*0.5:
        print('maxarea', max_area)
        print('HE/SHE DID IT!!!!! REPORT!!!')
        #return True
    else:
        print('maxarea', max_area)
        print(width*height*0.7)
        print('No violation')
        #return False
    
    #---- TEST CODE -------------
    mask = np.zeros(closing.shape, np.uint8)
    sorted_cnts = sorted(cnts, key=cv.contourArea, reverse=True)
    cv.drawContours(mask, [sorted_cnts[0]], 0, 255, -1)
    cv.drawContours(closing, sorted_cnts, 0, (128, 128, 128), 3)
    cv.imshow('foreground', mask)
    cv.waitKey(0)
    cv.destroyAllWindows()
    ################################

def main():
    
    #format: top_STREETNAME_DATE for top camera
    #format2: in_STREETNAME_DATE for inner camera

    # get information from the stream filename
    filename= ''
    items = filename.split('_')
    top = True if items[0] == 'top' else False
    street_name = items[1]
    date = items[2]


    video_path = "1.mp4"
    times = 0
    # street_name = cur_street

    frameFrequency = 30

    #TODO: DELET THIS
    outPutDirName = '/test_footage/test_frames'
    #####################################

    camera = cv.VideoCapture(video_path)
    while True:
        res, image = camera.read()
        times += 1
        if not res:
            # print('not res , not image')
            break   
        if times%frameFrequency == 0:
            cv.imwrite("/temp/" + str(times) + '.jpg', image)
        print(times)
    print('圖片提取結束')
    camera.release()

#detect_dump('full_white.jpg', 'full_black.jpg')
