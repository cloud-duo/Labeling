import json
import os

from flask import Flask, jsonify, abort
from google.cloud import storage
from google.cloud import vision

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/label/<id>', methods=['GET'])
def label(id):
    storage_client = storage.Client.from_service_account_json('keys.json')
    client = vision.ImageAnnotatorClient.from_service_account_json('keys.json')

    bucket_name = 'galeata_magica_123'

    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=id + "/")

    label_dict = dict()

    for blob in blobs:
        if blob.name[-1] == '/':
            continue
        uri = "gs://" + bucket_name + "/" + blob.name

        image = vision.types.Image()
        image.source.image_uri = uri

        response = client.label_detection(image=image)
        labels = response.label_annotations

        for label in labels:
            if label.description in label_dict:
                label_dict[label.description] += label.score
            else:
                label_dict[label.description] = label.score

    if not label_dict:
        abort(404)

    return jsonify(label_dict)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'this will be the labels!'

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
