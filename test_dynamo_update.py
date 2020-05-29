import boto3
from cv2 import cv2 as cv
import json
import csv


with open('C:/Users/alex5/Desktop/credentials.csv', 'r') as c:
    next(c)
    r = csv.reader(c)
    for l in r:
        kid = l[2]
        s_kid = l[3]


db = boto3.client('dynamodb', aws_access_key_id = kid, aws_secret_access_key = s_kid, region_name= "ap-northeast-2")
db.put_item(TableName = 'tyotdb',
    Item= {
        'img_name': {'S': 'test.jpg'},
        'Street': {'S': '測試'},
        'Date': {'N': '20200528'}
    }
)