import keras.models
from keras.models import model_from_json
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
import tensorflow as tf
import pickle


def init():
    json_file = open('resources/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json, custom_objects={'CRF':CRF})
    loaded_model.load_weights("resources/lstm_crf_weights.h5")
    print("\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   MODEL WAS SUCCESSFULLY LOADED! \n")
    loaded_model.compile(optimizer="rmsprop",loss=crf_loss)
    graph = tf.get_default_graph()

    print("\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   TAGS AND WORDS WAS SUCCESSFULLY LOADED! \n ")
    with open("resources/tag_to_index.pickle", "rb") as tags:
        idx2tag = pickle.load(tags)

    with open("resources/word_to_index.pickle", "rb") as words:
        word2idx = pickle.load(words)

    return loaded_model, graph, idx2tag, word2idx
