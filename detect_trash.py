import csv
import boto3
import json
import numpy as np
from cv2 import cv2 as cv
import os

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
    kernel = np.ones((10,10), np.uint8)
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
        print('maxarea', max_area)
        print('HE/SHE DID IT!!!!! REPORT!!!')
        #return True
    else:
        print('maxarea', max_area)
        print('No violation')
        #return False
    
    #---- TEST CODE -------------
    cv.imshow('foreground', opening)
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
    outPutDirName = 'C:/Users/Leo Kuo/Desktop/ytot test/' + sourceFileName + '/'

    if not os.path.exists(outPutDirName):
        os.mkdir(outPutDirName)
        print("該檔案已建立")
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

def upload2S3(bucket_name, file_name, file_path) :
    s3 = boto3.client('s3',
                        aws_access_key_id = kid,
                        aws_secret_access_key = s_kid)

    s3.upload_file(file_path, bucket_name, file_name)

def upload2DB(table_name, Street, p_img, obj_img, Date):
    db = boto3.client('dynamodb', aws_access_key_id = kid, aws_secret_access_key = s_kid, region_name= "ap-northeast-2")
    db.put_item(TableName = table_name,
        Item= {
            'p_img': {'S': p_img},
            'obj_img': {'S': obj_img},
            'Street': {'S': Street},
            'Date': {'N': Date}
        }
    )


if __name__ == "__main__":
    s3 = boto3.client('s3', aws_access_key_kid = kid, aws_secret_access_key= s_kid)



