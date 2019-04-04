import os

from flask import Flask
from google.cloud import storage

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/label/<id>', methods=['GET'])
def label(id):
    storage_client = storage.Client.from_service_account_json('keys.json')

    bucket_name = 'galeata_magica_123'

    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=id)

    for blob in blobs:
        if blob.name[-1] == '/':
            continue
        if not os.path.exists(id):
            os.mkdir(id)
        blob.download_to_filename(blob.name)

    return ''


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'this will be the labels!'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
