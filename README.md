# tyot
throw your own trash

# Description
A project designed to prevent Taipei citizens from throwing household garbage into public trash cans using Amazon Rekognitnion.

# How it's built
Sicne we can not find live stream cam avaliavle for our purpose, we use S3 bucket and trigger to simulate the process of a live stream

Video -> Lambda -> runs foreground detection with opencv -> oploads data to S3 bucket and DynamoDB
Front end:
button click -> API CALL -> fetch images

# Test it your self
you can test the project yourself with our front end:
https://ahsieh53632.github.io/tyotsite/
