### Text mining, Lab 2
### Nadine Enning, Niels van der Heijden, Ruth Wijma
### Group 16

import nltk
# assignment 1

text = '''Next, in named entity recognition, we segment and label the entities that might participate
	in interesting relations with one another. Typically, these will be definite noun
	phrases such as the knights who say “ni”, or proper names such as Monty Python. In
	some tasks it is useful to also consider indefinite nouns or noun chunks, such as every
	student or cats, and these do not necessarily refer to entities in the same way as definite
	NPs and proper names.
	Finally, in relation extraction, we search for specific patterns between pairs of entities
	that occur near one another in the text, and use those patterns to build tuples recording
	the relationships between the entities.'''

tokens = nltk.word_tokenize(text)
porter = nltk.PorterStemmer()
stems = [porter.stem(token) for token in tokens]


# assignment 2

from bs4 import BeautifulSoup
import urllib.request
import re

html = urllib.request.urlopen('https://www.elle.com/beauty/health-fitness/a28600/amanda-chantal-bacon-moon-juice-food-diary/')

parser = BeautifulSoup(html, 'html.parser')

texts = parser.findAll('p', attrs = {'class':'body-text'})

# remove empty tags
texts = [text for text in texts if len(text) > 0]

# remove HTML tags
texts = [re.sub(r"<.*?>", "", str(text)) for text in texts]

tokens = []

for text in texts:
	tokens += nltk.word_tokenize(text)

print(nltk.pos_tag(tokens))
