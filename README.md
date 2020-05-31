# tyot
throw your own trash

# Description
A project designed to prevent Taipei citizens from throwing household garbage into public trash cans using Amazon Rekognitnion.

# How it's built
Sicne we can not find live stream cam avaliavle for our purpose, we use a S3 bucket and a trigger to simulate the process of a live stream.
We realized that Amazon rekognition cannot detect plastic bags well, and it's incapable of detecting "dump" actions. Therefore, we implemented foreground detection with opencv in this project. An object is considered household garbage if its size reaches a threshold.

# How to use
All you need to do is upload the video to the "tyotinput" bucket and our lambda function will handle the rest
Note: tyotinput bucket is not public
# Architec:
Video -> Lambda -> runs foreground detection with opencv -> oploads data to S3 bucket and DynamoDB
Front end:
button click -> API CALL -> fetch images

# Test it your self
you can test the project yourself with our front end:
Note: Our S3 bucket for input isn't public, which means you can not upload your own test files

First you enter the desired address, then you selected searching option: you can find all violations that occured at that street or find violations between a specific time frame. Finally, click submit and you should get the image of the person, and what he/she threw, in a table format 
https://ahsieh53632.github.io/tyotsite/
