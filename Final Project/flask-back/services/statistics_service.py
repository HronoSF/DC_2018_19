import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import string
from nltk.tokenize import sent_tokenize


def count_statistic(filename,txt):
    from .predictions_service import get_tags_to_str_input
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
    generate_pie(output,filename)


def generate_pie(output, filename):

    labels = []
    values = []

    for entry in [output]:
        [labels.append(name) for name in entry.keys()]
        [values.append(count) for count in entry.values()]

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    ax.pie(values, labels=labels, autopct='%1.1f%%',
           shadow=True, startangle=90)
    plt.savefig('resources/statistics/'+filename+'.png')
