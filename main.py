import tweepy
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd


ckey     = "KayK96gy2XEcBemrZqZyAN73x"
csecret  = "4aVszACN3ns041h20GGTIeqM04KoE2VtM2jyjAE5ZKKbBsvBEJ"
atoken   = "21410208-MInctRmbtydglWeLs90WbhirQ5vj5cUoitbgp6ekO"
asecret  = "9mW1BYCWbBXoMuFQylN4Vz6DEO84FGvaCLSlYDxTZ1X0B"

def get_all_tweets(screen_name):
	# Twitter only allows access to a users most recent 3240 tweets with this method
	
	# authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	api = tweepy.API(auth)
	
	# initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	# make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=199)
	
	# save most recent tweets
	alltweets.extend(new_tweets)
	
	# save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	# keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
	
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=199,max_id=oldest, tweet_mode='extended')
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

	# print total tweets fetched from given screen name
	print("Total tweets downloaded from %s are %s" % (screen_name,len(alltweets)))
	
	return alltweets


# tweets_trump = get_all_tweets('BarackObama')

# with open('obama2_.txt', 'w') as f:
# 	for tweet in tweets_trump:
# 		json.dump(tweet._json, f)
# 		# f.write('\n')
tweets_obama = get_all_tweets('BarackObama')

df = pd.DataFrame({'source':[],
                   'text':[],
                   'created_at':[],
                   'retweet_count':[],
                   'favorite_count':[],
                   'is_retweet':[],
                   'id_str':[]})

for tweet in tweets_obama:
    t = tweet._json
    
    df = df.append({'source':t['source'],
                    'text':t['full_text'],
                    'created_at':t['created_at'],
                    'retweet_count':t['retweet_count'],
                    'favorite_count':t['favorite_count'],
                    'is_retweet':t['retweeted'],
                    'id_str':t['id_str']}, ignore_index = True)

analyzer = SentimentIntensityAnalyzer()

df['sentiment'] = df.text.apply(lambda t: analyzer.polarity_scores(t)['compound'])


df.to_csv('obama_sentiment_full.csv', sep=';')