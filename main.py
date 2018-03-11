import tweepy
import json


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
		new_tweets = api.user_timeline(screen_name = screen_name,count=199,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

	# print total tweets fetched from given screen name
	print("Total tweets downloaded from %s are %s" % (screen_name,len(alltweets)))
	
	return alltweets


tweets_trump = get_all_tweets('BarackObama')

with open('obama.txt', 'w') as f:
	for tweet in tweets_trump:
		json.dump(tweet._json, f)


