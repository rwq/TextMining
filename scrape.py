from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import time

ckey     = "KayK96gy2XEcBemrZqZyAN73x"
csecret  = "4aVszACN3ns041h20GGTIeqM04KoE2VtM2jyjAE5ZKKbBsvBEJ"
atoken   = "21410208-MInctRmbtydglWeLs90WbhirQ5vj5cUoitbgp6ekO"
asecret  = "9mW1BYCWbBXoMuFQylN4Vz6DEO84FGvaCLSlYDxTZ1X0B"



class listener(StreamListener):

	def on_status(self, status):

		if status.coordinates:
			print(status.coordinates)
		if status.place:
			print(status.place)

	def on_data(self, data):
		# print(data)
		# return True
		try:			
			# f = open('tweets.csv', 'a')
			# f.write(data)
			# f.write('\n')
			# f.close()

			# if data.location:
			# 	print(data.location)
			# if data.coordinates:
			# 	print(data.coordinates)
			# if data.place:
			# 	print(data.place)



			return True
		except BaseException as e:
			print('failed ondata: ', str(e))
			time.sleep(100)
			return True


	def on_error(self, status):
		print('status:', status)


auth = OAuthHandler(ckey, csecret)
api = tweepy.API(auth)

cursor = tweepy.Cursor(api.search, q='gemeenteraadsverkiezingen', rpp=100, wait_on_rate_limit=True).items()

f = open('times3.txt', 'w')



for tweet in cursor:
	f.write(str(tweet.created_at))
	f.write('\n')

# auth.set_access_token(atoken, asecret)
# twitter_stream = Stream(auth, listener())
# twitter_stream.filter(track=['Gemeenteraadsverkiezingen'])