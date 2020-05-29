import cv2
import os
import boto3

def splitFrames_mp4(sourceFileName, cur_street):

    video_path = "1.mp4"
    times = 0
    # street_name = cur_street


    # 每25禎提取一次
    # frameFrequency = 25

    outPutDirName = 'C:/Users/Leo Kuo/Desktop/ytot test/' + sourceFileName + '/'

    if not os.path.exists(outPutDirName):
        os.mkdir(outPutDirName)
        print("該檔案已建立")

    camera = cv2.VideoCapture(video_path)
    while True:
        times+=1
        res, image = camera.read()
        if not res:
            # print('not res , not image')
            break

        # if times%frameFrequency==0:
        #     cv2.imwrite(outPutDirName + str(times)+'.jpg', image)
        #     print(outPutDirName + str(times)+'.jpg')

        cv2.imwrite(outPutDirName + str(times) + '.jpg', image)
        print(times)
    print('图片提取结束')
    camera.release()

def upload2S3(access_key, secret_password, bucket_name, cur_file_path, file_name) :

    aws_access_key = access_key

    aws_secret_password = secret_password

    s3_bucket_name = bucket_name

    file_path = cur_file_path

    file = file_name

    s3 = boto3.resource('s3',
                        aws_access_key_id = aws_access_key,
                        aws_secret_access_key = aws_secret_password)

    s3.Object(bucket_name, file_name).put(Body = file)

def upload2DB()
splitFrames_mp4('test1')