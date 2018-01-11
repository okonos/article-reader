import boto3
import hashlib
from flask import Flask, render_template, request, redirect
from flask_s3 import FlaskS3
from newspaper import Article


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
        voice = request.form['voiceSelect']
        url = request.form['url']
        a = Article(url)
        a.download()
        a.parse()
        text = a.text
        # TODO error handling
        # if not text...

        speech = b''
        chunkSize = 1200
        while text:
            i = text[chunkSize:].find('.') + 1
            chunk = text[:chunkSize+i]
            chunk = '<speak><p>' + chunk.replace('\n\n', '</p><p>') + \
                '</p></speak>'
            text = text[chunkSize+i:].strip()
            response = polly.synthesize_speech(
                OutputFormat='mp3',
                Text=chunk,
                TextType='ssml',
                VoiceId=voice
            )
            speech += response['AudioStream'].read()

        hashInput = url + voice
        filename = hashlib.md5(hashInput.encode('utf-8')).hexdigest() + '.mp3'
        s3.put_object(Bucket=BUCKET_NAME, Key=filename,
                      Body=speech,
                      ContentType='audio/mpeg',
                      ACL='public-read')
        return redirect(BUCKET_URL + filename)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
