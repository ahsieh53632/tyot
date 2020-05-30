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
        print('maxarea', max_area)
        print('HE/SHE DID IT!!!!! REPORT!!!')
        return True
    else:
        print('maxarea', max_area)
        print('No violation')
        return False
    
    # #---- TEST CODE -------------
    # cv.imshow('foreground', opening)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    # ################################

def main(top_view, in_view, bucket):
    
    #format: top_STREETNAME_DATE for top camera
    #format2: in_STREETNAME_DATE for inner camera

    # get information from the stream filename
    items = top_view.split('_')
    street_name = items[1]
    date = items[2]

    # get video files from the bucket
    s3 = boto3.resource('s3')
    s3.meta.client.download_file(bucket, top_view, '/temp/' + top_view)
    s3.meta.client.download_file(bucket, top_view, '/temp/' + in_view)
    times = 0
    # street_name = cur_street
    frameFrequency = 10
    #####################################

    camera_top_view = cv.VideoCapture('/temp/' + top_view)
    camera_in_view = cv.VideoCapture('/temp/' + in_view)
    res_top_view, frame_top_view = camera_top_view.read()
    res_in_view, frame_in_view = camera_in_view.read()

    if not (res_in_view and res_top_view):
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
            if (pause > 0):
                pause -= 1
            else:
                if (detect_dump(frame_in_view, last)):
                    obj_name = 'obj_' + str(uuid.uuid4()) + '.jpg'
                    p_name = 'person_' + str(uuid.uuid4()) + '.jpg'
                    obj_path = "/temp/" +  obj_name
                    p_path = "/temp/" + p_name
                    cv.imwrite(obj_path, frame_in_view)
                    cv.imwrite(p_path, frame_top_view)
                    # upload files to bucket
                    upload2S3(bucket, obj_name, obj_path)
                    upload2S3(bucket, p_name, p_path)
                    # upload to DB
                    upload2DB('tyotdb', street_name, p_name, obj_name, date)
                    # skip 2 frames to avoid redundant searches
                    pause = 2
    camera_top_view.release()
    camera_in_view.release()

def upload2S3(bucket_name, file_name, file_path) :
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, file_name)

def upload2DB(table_name, Street, p_img, obj_img, Date):
    db = boto3.client('dynamodb', region_name= "ap-northeast-2")
    db.put_item(TableName = table_name,
        Item= {
            'p_img': {'S': p_img},
            'obj_img': {'S': obj_img},
            'Street': {'S': Street},
            'Date': {'N': Date}
        }
    )


def find_item(name, obj_list):
    for i in obj_list['Contents']:
        if i['key'] == name:
            return True
    return False

def lambda_hanlder(event, context):
    s3 = boto3.client('s3')
    top_view = ''
    in_view = ''

    record = event['Records'][0]
    bucket = record['bucket']['name']
    srckey = unquote_plus(record['s3']['object']['key'])
    
    
    l = s3.list_objects(Bucket=bucket)
    # checking if this object is top view or in view
    if srckey[0:3] == 'top':
        top_view = srckey
        to_find = 'in' + srckey[3:]
        if (not find_item(to_find, l)):
            print('not found:' + to_find)
            return
        else:
            in_view = to_find
    else:
        in_view = srckey
        to_find = 'top' + srckey[3:]
        if (not find_item(to_find, l)):
            print('not found:' + to_find)
            return
        else:
            top_view = to_find

    # guaranted that both video exsists in S3 bucket
    main(top_view, in_view, bucket)