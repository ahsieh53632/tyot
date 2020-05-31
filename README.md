# tyot
throw your own trash

# Description
A project designed to prevent Taipei citizens from throwing household garbage into public trash cans

# Design
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

# Pre-req
If you want to run this project locally, make sure you have opencv-python installed

# How to use
All you need to do is upload the video to the "tyotinput" bucket and our lambda function will handle the rest <br />
Note: tyotinput bucket is not public at this moment

# Test it your self
you can test the output of our test video with our front end:

First you enter the desired address
then you selected searching option: you can find all violations that occured at that street or find violations between a specific time frame. 
Finally, click submit and you should get the image of the person, and what he/she threw, in a table format 
https://ahsieh53632.github.io/tyotsite/
