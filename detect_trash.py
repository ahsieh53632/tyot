import csv
import boto3
import json
import numpy as np
from cv2 import cv2 as cv


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
    
    print('found cnts')
    max_area = 0
    sorted_cnts = sorted(cnts, key=cv.contourArea, reverse=True)

    cv.drawContours(closing, sorted_cnts, 0, (128, 128, 128), 3)
    if (len(cnts) > 0):
        for c in cnts:
            curr = cv.contourArea(c)
            max_area = max(max_area, curr)
    if max_area > width*height*0.7:
        print('maxarea', max_area)
        print('HE/SHE DID IT!!!!! REPORT!!!')
    else:
        print(width*height*0.5)
        print('maxarea', max_area)
        print('No violation')

    
    #---- TEST CODE -------------
    cv.imshow('foreground', closing)
    cv.waitKey(0)
    cv.destroyAllWindows()
    ################################

if __name__ == "__main__":
    detect_dump('curr.jpg', 'last.jpg')

