import boto3
import hashlib
from flask import Flask, render_template, request, redirect
from flask_s3 import FlaskS3


app = Flask(__name__)
BUCKET_NAME = 'reader-app-bucket'
app.config['FLASKS3_BUCKET_NAME'] = BUCKET_NAME
f_s3 = FlaskS3(app)
s3 = boto3.client('s3')
REGION = s3.get_bucket_location(Bucket=BUCKET_NAME)['LocationConstraint']
BUCKET_URL = 'https://s3.' + REGION + '.amazonaws.com/' + BUCKET_NAME + '/'
polly = boto3.client('polly')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        response = polly.synthesize_speech(
            OutputFormat='mp3',
            Text=text,
            TextType='text',  # 'ssml',
            VoiceId='Joanna'
        )
        filename = hashlib.md5(text.encode('utf-8')).hexdigest() + '.mp3'
        s3.put_object(Bucket='reader-app-bucket', Key=filename,
                      Body=response['AudioStream'].read(),
                      ContentType='audio/mpeg',
                      ACL='public-read')
        return redirect(BUCKET_URL + filename)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
