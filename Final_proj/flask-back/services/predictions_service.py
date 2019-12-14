from flask.helpers import send_file
import io
import nltk
from models.initialize import init
import keras.models
from keras.preprocessing.sequence import pad_sequences


import numpy as np

from .statistics_service import count_statistic

import re
import sys
import string

import os
from os import path

sys.path.append("/")

nltk.download('punkt')


global model, graph
model, graph, idx2tag, word2idx = init()

MAX_LEN = 75
UPLOAD_FOLDER = 'uploaded/'

re_tok = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')


def preprocess_data(data): return re_tok.sub(r' \1 ', data).split()


def get_tags_to_str_input(input_data):
    output_data = []
    preprocessed_data = preprocess_data(input_data)

    x_test_sent = pad_sequences(sequences=[[word2idx.get(w, 0) for w in preprocessed_data]],
                                padding="post", value=word2idx["PAD"], maxlen=MAX_LEN)

    with graph.as_default():
        out = model.predict(np.array([x_test_sent[0]]))
        out = np.argmax(out, axis=-1)

        for word, prediction in zip(preprocessed_data, out[0]):
            entry = {
                'word': word,
                'tag': idx2tag[prediction]
            }
            output_data.append(entry)

        return output_data


def get_tags_to_file_input(path_to_file, filename):
    input = open(path_to_file, encoding='utf-8').read()
    count_statistic(filename,input)
    return send_file('resources/statistics/'+filename+'.png', attachment_filename='statistic.jpg')
