import os
import io
import re
import sys
import nltk
import string
import numpy as np
import keras.models
import pandas as pd
from os import path
import matplotlib.pyplot as plt
from models.initialize import init
from flask.helpers import send_file
from matplotlib.figure import Figure
from nltk.tokenize import sent_tokenize
from keras.preprocessing.sequence import pad_sequences
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

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

def count_statistic(filename,txt):
    i=0;
    output = {}
    for sentence in sent_tokenize(txt):
        sentence = sentence.translate(
            str.maketrans('', '', string.punctuation))
        word_to_tag = get_tags_to_str_input(sentence)
        for word in word_to_tag:
            if word.get('tag') == "PER":
                if word.get('word') in output:
                    output[word.get('word')] += 1
                    print("Increase")
                else:
                    output[word.get('word')] = 1
                    print("added")
            i+=1
            if (i>100): break;
    generate_pie_diagram(output,filename)

def generate_pie_diagram(output, filename):

    names = []
    frequency = []

    for entry in [output]:
        [names.append(name) for name in entry.keys()]
        [frequency.append(count) for count in entry.values()]
    
    df=pd.DataFrame(
    data = {'frequency': frequency, 'name' : names},
    ).sort_values('value', ascending = False)
    df2 = df[:10].copy()
    

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    ax.pie(df2['frequency'].tolist(), labels=df2['name'].tolist(), autopct='%1.1f%%',
           shadow=True, startangle=90)
    plt.savefig('resources/statistics/'+filename+'.png')

