#trump analysis
import pandas as pd
from datetime import datetime
from dateutil import parser
import matplotlib.pyplot as plt
import nltk
from geopy.geocoders import Nominatim
import pygal
import numpy as np
import time
import pickle
from geopy.exc import GeocoderServiceError


# import data
trump = pd.read_csv('c:/users/ruth/documents/master/textmining/project/data/trump_sentiment_2.csv', sep=';', lineterminator='\n')
obama = pd.read_csv('c:/users/ruth/documents/master/textmining/project/data/obama_sentiment.csv', sep=';')


# convert time
trump['created_at'] = trump.created_at.apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M:%S'))
trump['hour_of_day'] = trump.created_at.apply(lambda ca: ca.hour)
trump = trump.set_index('created_at')
trump['sentiment'] = trump['sentiment\r']
del trump['sentiment\r']

obama['created_at'] = obama.created_at.apply(lambda t: parser.parse(t))
obama['hour_of_day'] = obama.created_at.apply(lambda ca: ca.hour)
obama = obama.set_index('created_at')






def get_locations_from_chunks(chunk):
	# for chunk in chunks:
	locations = []
	for st in chunk.subtrees(filter=lambda x: x.label() == 'GPE'):
		location = str()
		entities = str(st).split()[1:]

		if len(entities) == 1:
			location = entities[0].split('/')[0]

		else:			
			for entity in entities:
				location += entity.split('/')[0]

		locations.append(location)

	return locations

def get_countrycode_from_location(location):
	if location in country_codes:
		return country_codes[location]
	try:
		time.sleep(1)
		geo_object = geocoder.geocode(location)
		lat, lon = geo_object.latitude, geo_object.longitude
		country_info = geocoder.reverse('{}, {}'.format(lat,lon))
		country_code = country_info.raw['address']['country_code']

		country_codes[location] = country_code

		return country_code
	except GeocoderServiceError:
		wait_sec = 30
		print('Waiting {} secs for API'.format(wait_sec))
		time.sleep(wait_sec)
		return get_countrycode_from_location(location)



# select dataset
name = 'trump'




if name == 'obama':
	df=obama
else:
	df=trump


# init
country_codes = {}
geocoder = Nominatim()
country_sentiment = {}
mean_sentiment = {}
locations_mentioned = []


i = 0
t = time.time()

for index, row in df.iterrows():
	tweet = row.text
	sentiment = row.sentiment

	tokens = nltk.word_tokenize(tweet)
	tags = nltk.pos_tag(tokens)
	chunk = nltk.ne_chunk(tags)

	locations = get_locations_from_chunks(chunk)

	for location in locations:
		print(location)
		try:
			country_code = get_countrycode_from_location(location)

			locations_mentioned.append(location)

			if country_code in country_sentiment:
				country_sentiment[country_code].append(sentiment)
			else:
				country_sentiment[country_code] = [sentiment]

		except Exception as e:
			print(e)

	if i%100 == 0:
		elapsed = time.time() - t
		print('{} done in {} sec'.format(i, elapsed))
	i += 1




# replace by mean per country
for key in country_sentiment:
	mean_sentiment[key] = np.mean(country_sentiment[key])
	
	

print(country_sentiment)

positive = {key: mean_sentiment[key] for key in mean_sentiment if mean_sentiment[key] > 0}
negative = {key: mean_sentiment[key] * -1 for key in mean_sentiment if mean_sentiment[key] < 0}

with open('{}_country'.format(name), 'wb') as f:
	pickle.dump(country_sentiment, f)

with open('{}_locations_mentioned'.format(name), 'wb') as f:
	pickle.dump(locations_mentioned, f)


# charts
worldmap_chart = pygal.maps.world.World()
worldmap_chart.title = 'Sentiment by country'
worldmap_chart.add('positive', positive)
worldmap_chart.add('negative', negative)
worldmap_chart.render_to_file('{}.svg'.format(name))