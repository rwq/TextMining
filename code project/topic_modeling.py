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
import re

exclude_words = ['https', 'amp', 'rt', 'RT', 'co', 'CO', 'http', 'obama', 'trump', 'BarackObama', 'RealDonaldTrump', 'Trump', 'Obama']
# clean data by removing stop words and punctuation



###################################################
# Functions
###################################################

def clean(doc):
    #init sets to filter on
    stop = set(stopwords.words('english'))
    stop.update(exclude_words) 
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    #apply filters and lemmatization
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = [lemma.lemmatize(word) for word in punc_free.split()]
    normalized = [i for i in normalized if i not in stop]
    
    ###VERSION 1: FIRST STOPWORDS, PUNCTUATION AND LEMMATIZATION IS GOTTEN OUT.###
    # tagged = nltk.pos_tag(normalized)
    # namedEnt = nltk.ne_chunk(tagged, binary = True)
    # nouns = re.findall(r'\b(.*?)/NN', str(namedEnt))
    # return nouns

    ###VERSION 2: ONLY TOKENIZED###
    tokenized = nltk.word_tokenize(doc)
    tagged = nltk.pos_tag(tokenized) 
    namedEnt = nltk.ne_chunk(tagged, binary = True)
    nouns = re.findall(r'\b(.*?)/NN', str(namedEnt))  
    nouns_without_ne = [re.findall(r'NE\s(.*)', str(word))[0] if word.startswith('NE ') else word for word in nouns]
    nouns_without_ne = [noun for noun in nouns_without_ne if noun not in exclude_words] 
    return nouns_without_ne

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
    

def  create_wc(text,mask_path = '', max_words = 1000):
    sw = STOPWORDS

    if mask_path == '':
        wc = WordCloud(max_words = max_words, stopwords=sw, margin=10, random_state=1).generate(text)
    else:
        mask = np.array(Image.open(mask_path)) 
        wc = WordCloud(max_words = max_words, mask=mask, stopwords=sw, margin=10, random_state=1).generate(text)

    default_colors = wc.to_array()

    plt.figure()
    plt.title("Default colors")
    plt.imshow(default_colors, interpolation="bilinear")
    plt.axis("off")
    plt.show() 


''' ###################################################
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
plt.show() '''