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

# moving average
trump['moving_avg'] = trump.sentiment.rolling(window=500, min_periods=10).mean()
obama['moving_avg'] = obama.sentiment.rolling(window=500, min_periods=10).mean()

fig, ax = plt.subplots()

trump['moving_avg'].plot(ax = ax, color='red')
obama['moving_avg'].plot(ax = ax, color='blue')

handles, labels = ax.get_legend_handles_labels()

ax.legend(handles, ['Trump', 'Obama'])
ax.set_xlabel('Time')
ax.set_ylabel('Sentiment')
ax.set_title('Moving average of sentiment')

plt.axvline(x='08-11-2016', linestyle='--')

plt.show()