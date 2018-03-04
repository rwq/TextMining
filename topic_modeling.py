import numpy as np
import nltk

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string

import gensim
from gensim import corpora
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import tkinter

doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle."

# compile documents
doc_complete = [doc1, doc2, doc3, doc4, doc5]

# clean data by removing stop words and punctuation



###################################################
# Functions
###################################################

def clean(doc):
    #init sets to filter on
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()

    #apply filters and lemmatization
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = [lemma.lemmatize(word) for word in punc_free.split()]
    return normalized

def clean_doc_list(doc_list):
    return [clean(doc) for doc in doc_list]

def get_doc_term_matrix_and_dict(doc_list):
    dictionary = corpora.Dictionary(doc_list)

    return [dictionary.doc2bow(doc) for doc in doc_list], dictionary


def get_topics(doc_term_matrix, nr_topics, dictionary, nr_passes, nr_words):
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=nr_topics, id2word = dictionary, passes=nr_passes)

    return ldamodel.print_topics(num_topics = nr_topics, num_words = nr_words)
    


###################################################
# Practice
###################################################
normalized = clean_doc_list(doc_complete)
print(normalized)
print(type(normalized))
doc_term_matrix, dictionary = get_doc_term_matrix_and_dict(normalized)

topics = get_topics(doc_term_matrix, 3, dictionary, 100, 3)

print(topics)


###################################################
# Wordcloud creation
###################################################
d = path.dirname(__file__)

mask = np.array(Image.open(path.join(d, "obama.jpg"))) 

print(np.sum(mask))
sw = STOPWORDS

text = open('obamaspeech.txt').read()

wc = WordCloud(max_words = 1000, mask=mask, stopwords=sw, margin=10, random_state=1).generate(text)

default_colors = wc.to_array()

plt.figure()
plt.title("Default colors")
plt.imshow(default_colors, interpolation="bilinear")
plt.axis("off")
plt.show()