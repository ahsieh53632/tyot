# TYOT: Throw Yoyr Own Trash!

## Description
A project designed to prevent Taipei citizens from throwing household garbage into public trash cans

## Built With
AWS api gateway <br />
AWS lambda <br />
AQWS DynamoDB <br />
Opencv Library <br />
Aws S3 Bucket

## Design
Sicne we can not find avaliavle live stream cams  for our purpose, we use a S3 bucket and a trigger to simulate the process of a live stream.
We realized that Amazon rekognition cannot detect plastic bags well, and it's incapable of detecting "dump" actions. 
Therefore, we implemented foreground detection with opencv in this project. 
An object is considered household garbage if its size reaches a threshold.

Simplified Architec of this project:
```
Video -> Lambda -> runs foreground detection with opencv -> uploads data to S3 bucket and DynamoDB
Front end:
button click -> API CALL -> fetch images
```

## Pre-req
If you want to run this project locally, make sure you have opencv-python installed

## How to use
All you need to do is upload your test video to the "tyotinput" bucket and our lambda function will handle the rest <br />
Then you can fetch images from DynamoDB using our front end
##### Note: tyotinput bucket is not public at this moment

## Test it your self
you can see the output of our test videos with our front end: https://ahsieh53632.github.io/tyotsite/  <br />
our test-video link: https://drive.google.com/file/d/1zbplH_ehZaSC7dV1mxNm-LseNiswpQNK/view?usp=sharing
```
Type 中央路 for the street name
Currently we only have data for the dates 20200532 
``` 
then, click submit and you should get images of individuals who dumped household garbage, and the objects that they threw 

you can also test it with your own video files using run_locally.py
