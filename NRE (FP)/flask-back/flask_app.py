import re
import os
import sys
import string

from flask import Flask, request, redirect, url_for, jsonify
from flask_cors import CORS

from services.functional import *
UPLOAD_FOLDER = 'uploaded/'

if not(os.path.exists(UPLOAD_FOLDER)):
        os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app)


@app.route('/predict_str', methods=['GET', 'POST'])
def predict_str():
    if request.method == 'POST':
        input_data = request.get_json()['data']
        return jsonify(get_tags_to_str_input(input_data))


@app.route('/predict_file', methods=['POST'])
def predict_file():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return get_tags_to_file_input(os.path.join(UPLOAD_FOLDER, filename),filename)


if __name__ == '__main__':
    app.run(port='5000', host='0.0.0.0')
