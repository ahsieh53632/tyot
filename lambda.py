import csv
import boto3
import json
import numpy as np
from cv2 import cv2 as cv
import os
from urllib.parse import unquote_plus
import uuid

def detect_dump(curr, last):
    sub = cv.createBackgroundSubtractorMOG2()
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
    cv.drawContours(curr, sorted_cnts, 0, (0, 0, 255), 3)
    # find area in dump area
    if (len(sorted_cnts) > 0):
        mask = np.zeros(opening.shape, np.uint8)
        cv.drawContours(mask, [sorted_cnts[0]], 0, 255, -1) 
        crop_x_start = 500
        crop_x_end = 580
        crop_y_start = 800
        crop_y_end = 1380
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

def main(view, bucket):
    
    #format: STREETNAME_DATE for top camera
    # get information from the stream filename
    items = view.split('_')
    street_name = items[0]
    date = items[1].split('.')[0]
    
    print('street', street_name)
    print('date', date)
    # get video files from the bucket
    s3 = boto3.client('s3')
    f = '/tmp/' + str(view)
    print(f)
    
    s3.download_file(Bucket=bucket, Key=view, Filename=f)
    times = 0
    frameFrequency = 10
    #####################################

    camera = cv.VideoCapture(f)
    res, frame = camera.read()

    if not res:
        return 
    last = frame
    last_face = frame
    pause = 0

    # skip one frame
    res, frame = camera.read()
    while True:
        res, frame = camera.read()
        times += 1
        if not res:
            # print('not res , not image')
            break   
        if times%frameFrequency == 0:
            if (pause > 0):
                pause -= 1
            else:
                if (detect_dump(frame, last)):
                    obj_name = 'obj_' + str(uuid.uuid4()) + '.jpg'
                    p_name = 'person_' + str(uuid.uuid4()) + '.jpg'
                    obj_path = "/tmp/" +  obj_name
                    p_path = "/tmp/" + p_name
                    cv.imwrite(p_path, last_face)
                    cv.imwrite(obj_path, frame)
                    # upload files to bucket
                    upload2S3('tyotimg1', obj_name, obj_path)
                    upload2S3('tyotimg1', p_name, p_path)
                    # upload to DB
                    upload2DB('tyotdb', street_name, p_name, obj_name, date)
                    # skip 2 frames to avoid redundant searches
                    pause = 4
        if times%(frameFrequency*1.5) == 0:
            last_face = frame
    camera.release()
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

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    view = ''

    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    srckey = unquote_plus(record['s3']['object']['key'])
    
    view = srckey
    # l = s3.list_objects(Bucket=bucket)
    # # checking if this object is top view or in view
    # if srckey[0:3] == 'top':
    #     top_view = srckey
    #     to_find = 'in' + srckey[3:]
    #     if (not find_item(to_find, l)):
    #         print('not found:' + to_find)
    #         return
    #     else:
    #         in_view = to_find
    # else:
    #     in_view = srckey
    #     to_find = 'top' + srckey[3:]
    #     if (not find_item(to_find, l)):
    #         print('not found:' + to_find)
    #         return
    #     else:
    #         top_view = to_find
    print('view', view)
    print('bucket', bucket)
    main(view, bucket)