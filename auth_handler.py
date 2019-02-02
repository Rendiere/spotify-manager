from flask import Flask, request
from google.cloud import storage

app = Flask(__name__)
client = storage.Client()

BUCKET_ID = 'lekker-spotify-bucket-01'

@app.route('/callback')
def auth_test():
    print('ping')
    code = request.args.get('code')

    # TODO: Upload code to Google Cloud bucket
    # bucket = client.get_bucket(BUCKET_ID)
    # blob = bucket.blob('token.txt')
    # blob.upload_from_string(code)

    return code
