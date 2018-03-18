import topic_modeling as tp 
import pandas as pd
import re
import numpy as np
import ast

SUBJECTS_PER_TWEET = 1
WORDS_PER_TWEET = 3




############################################################
# Filter functions
############################################################
def filter_topic_words(lda_topics):
    topic_words = []
    for lda_topic in lda_topics:
        print(lda_topic)
        text = str(lda_topic[1])
        topic_words.append(re.findall(r'"(.*?)"',text))

    return topic_words



def filter_tweets(df, minimum):
    df['words'] =  df.text.apply(lambda x: str(x).split())
    df = df[df['words'].map(len) > minimum]

    df = df.drop('words', axis=1)

    return df

############################################################
# Find topic words per tweet
############################################################
  

def get_topic_words(tweet_df, min_words, person_name):
    tweet_df = filter_tweets(tweet_df, min_words)

    topics = []
    for _, row in tweet_df.iterrows():
        tweet = row.text
        normalized_tweet = tp.clean(tweet)
        doc_term_matrix, dictionary = tp.get_doc_term_matrix_and_dict([normalized_tweet])

        topic = tp.get_topics(doc_term_matrix, SUBJECTS_PER_TWEET, dictionary, 15, WORDS_PER_TWEET)
        #(print(row.text, topic))
        #rint(topic)
        topic_words = filter_topic_words([topic])[0]
        #print(topic_words)

        topics.append(topic_words)



    topic_words = pd.Series(topics)
    print(len(topic_words))
    print(len(tweet_df.text))
    tweet_df['topic_words'] = pd.Series(topics)
    path = './'+person_name+'_tweets_topics.csv'
    tweet_df.to_csv(path)

############################################################
# Create wordcloud from topic words df
############################################################
def get_tw_wc(tweets_path, mask_path, max_words = 1000):

    df = pd.read_csv(tweets_path, header = 0)
    #temp fix
    df = df.dropna(axis=0, how='any')

    text = []
    for _, row in df.iterrows():
        words = ast.literal_eval(row.topic_words)
        text.extend(words)


    text = ' '.join([word for word in text])
    tp.create_wc(text, mask_path)

############################################################
# Find most spoken of topics
############################################################
def get_topics(tweet_df, nr_topics, nr_words, nr_passes):
    tweets = tweet_df.text.tolist()
    normalized_tweets = tp.clean_doc_list(tweets)

    doc_term_matrix, dictionary = tp.get_doc_term_matrix_and_dict(normalized_tweets)
    topics = tp.get_topics(doc_term_matrix, nr_topics, dictionary, nr_passes, nr_words)

    return topics





############################################################
# Main
############################################################
''' 
df = pd.read_csv('./trump_tweets_topics.csv')
df.topic_words.apply(lambda x: filter_topic_words(np.array(x)))
print(df.head(10)) '''
trump_tweets = pd.read_csv('./data/trump_sentiment.csv', header = 0, sep=';')
trump_tweets = trump_tweets.dropna(axis=0, how='any')
print(trump_tweets.head(100))
trump_tweets['created_at'] = pd.to_datetime(trump_tweets['created_at'])
#get_topic_words(trump_tweets, 7, 'trump')
#get_tw_wc('/home/mrvoh/Documents/TextMining/ trump_tweets_topics.csv', mask_path='./trump.jpeg')









''' nr_topics_list = [10, 20, 30, 40, 50]
nr_words_list = [1,2,3,4,5]
nr_passes_list = [10,25,50]

for nr_topics in nr_topics_list:
    for nr_words in nr_words_list:
        for nr_passes in nr_passes_list:
            filepath = './topic_folder/'+str(nr_topics)+'-'+str(nr_words)+'-'+str(nr_passes)+'-trump.txt'
            with open(filepath, 'w') as f:
                raw_topics = get_topics(trump_tweets, nr_topics, nr_words, nr_passes)
                topics = filter_topic_words(raw_topics)
                f.write(str(topics))
 '''


