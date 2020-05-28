import csv
import boto3
import json
with open('C:/Users/alex5/Desktop/credentials.csv', 'r') as c:
    next(c)
    r = csv.reader(c)
    for l in r:
        kid = l[2]
        s_kid = l[3]

photo = 'test.jpg'

client = boto3.client('rekognition', aws_access_key_id = kid, aws_secret_access_key = s_kid)

with open(photo, 'rb') as p:
    b = p.read()

response = client.detect_labels(Image={'Bytes':b}, MinConfidence= 30)

for d in response['Labels']:
    if 'bag' in d['Name'] or 'Person' in d['Name']:
        print(d)