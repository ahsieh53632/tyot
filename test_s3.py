import boto3
from cv2 import cv2 as cv
import json
import csv

def test():
    with open('C:/Users/alex5/Desktop/credentials.csv', 'r') as c:
        next(c)
        r = csv.reader(c)
        for l in r:
            kid = l[2]
            s_kid = l[3]

    s3 = boto3.client('s3',
                        aws_access_key_id = kid,
                        aws_secret_access_key = s_kid)

    #TODO: FILENAME
    s3.upload_file('last.jpg', 'tyotimg1', 'last.jpg')
    #TODO: upload to dynamo DB

if __name__ == '__main__':
    a = 'top_abc_20200529'  
    print(a[0:3])