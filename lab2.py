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



texts = texts[0]

#for text in texts:
tokens = nltk.word_tokenize(texts)


tokens_pos = nltk.pos_tag(tokens)

chunks = nltk.ne_chunk(tokens_pos)
tagged_chunks = [chunk for chunk in chunks if type(chunk) != tuple]
#print(tagged_chunks)
''' Annotation guidelines:
For annotation we looped through all tokens in the text and annotated each token
if it is either (part of) a person (PERSON), location (GPE) or organization (ORGANIZATION)

 '''



''' CoNLL2003 format:
Token	POS-tag		Gold standard NER tag	Actual Tag
Poep	N			O						Person
 '''

#Manually annotate and store (token_index, tag)
gold_labels = [('Amanda',		'PERSON'),
				('Chantal',		'PERSON'),
				('Bacon', 		'PERSON'),
				('Moon',		'ORGANIZATION'),
				('Juice',		'ORGANIZATION'),
				('Los',			'GPE'),
				('Angeles',		'GPE'),
				('Gwyneth',		'PERSON'),
				('Paltrow',		'PERSON'),
				('Shailene',	'PERSON'),
				('Bacon',		'PERSON')]
 
gold_indices = {}
for token, tag in gold_labels:
	#print(tokens.index(token))
	try:
		gold_indices[tokens.index(token)] = tag
	except:
		print(token)

#add manualy since tokenizer fails to tokenize correctly
gold_indices[75] = 'ORGANIZATION'

#Connect tagged_chunks to original tokens to get token 
tagged_labels = {}
for chunk in tagged_chunks:
	for token, _ in chunk:
		try:
			tagged_labels[tokens.index(token)] = chunk._label
		except:
			print(token)

print((len(gold_indices), len(tagged_labels)))

#compare tagged and gold labels to get metrics
#recall
recalled_tokens = [key for key in gold_indices.keys() if (key in tagged_labels.keys() and tagged_labels[key] == gold_indices[key])]
recall = len(recalled_tokens) / len(gold_indices.keys())
print(recall)

#precision
correct_tags = [key for key in tagged_labels.keys() if (key in gold_indices.keys() and tagged_labels[key] == gold_indices[key])]
precision = len(correct_tags)/len(tagged_labels)
print(precision)


''' Qualitative analysis:
We found a recall of 0.8 and a precision of +- 0.67 which tells us that the used NER tagger 
tags more tokens than necessary. At least one mistake is probably caused by error propagation from the tokenizer,
since "Juice" in "Moon Juice" is not properly tokenized, this probably results into incorrect NER tagging.

 '''