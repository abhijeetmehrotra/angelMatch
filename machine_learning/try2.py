#skill bag of words
#cluster according to skills
#find the cluster that the user belongs to
#distance metric to determine how far from skill a user is
from collections import defaultdict
from gensim.models import Word2Vec
import pandas as pd
import numpy as np

peopleArray = {
  "person": [
    {
      "id": "12354678",
      "fname": "akshay",
      "lname": "nagpal",
      "skills": {
        "Matlab": "20",
        "CS": "10",
        "jQuery": "5"
      },
      "volunteer_experience": "4",
      "num_connections": "25",
      "location": "New York",
      "causes_supported": "Child Abuse Prevention,Literacy,Old Age People",
      "industry": "Computer Software",
      "summary": "I am a software engineer interested in full time roles. I also do volunteer work in my free time\""
    },
    {
      "id": "12354699",
      "fname": "siddharth",
      "lname": "bhatnagar",
      "skills": {
        "C++": "20",
        "CS": "10",
        "Python": "5"
      },
      "volunteer_experience": "4",
      "num_connections": "258",
      "location": "New York City",
      "causes_supported": "Child Abuse Prevention, Literacy, Old Age People",
      "industry": "Computer Science",
      "summary": "I am a software engineer interested in full time roles. I also do volunteer work in my free time\""
    }
  ]
}

skill_set_bow = []
l = dict(peopleArray['person'][1]['skills'])
for key, value in l.items():
	#print key, value
	skill_set_bow.append(key)

#print "######################"

#create data set
person_name = []
data = defaultdict(list)
count = 0
new_data = []
new_data_weights = []
for person in peopleArray['person']:
	name = person['fname'] + person['lname']
	person_name.append(name)
	new_data.append(person['skills'].keys())
	new_data_weights.append(person['skills'].values())
	person_skill = dict(person['skills'])
	for key, value in person_skill.items():
		data[name].append(key)

#print new_data
#print new_data_weights
#print data

print "####################"

final_data = []
for row in new_data:
	val = ''
	for v in row:
		val = val + v + ' '
	final_data.append(val)

#print final_data

print new_data
print "$$$$$$$$$$$$$$$$$$$$"

wv = Word2Vec(new_data, min_count = 1)#, size=100, window=5, min_count=5, workers=4)
#print wv.vocab
#print wv.most_similar('C++', topn = 3)


sentence = [['paris', 'london', 'new_york'], ['los_angeles', 'san_fransisco']]
w2v = Word2Vec(sentence, min_count = 1)
#print w2v.most_similar('europe', topn = 1)

skillset = pd.read_csv("skills.csv", delimiter=",")
w2v2_dataset = []
for val in skillset:
	w2v2_dataset.append(val)
w2v2 = Word2Vec(w2v2_dataset, min_count = 1)
#print len(w2v2_dataset)
#print w2v2_dataset
#print len(w2v2.vocab)

model = Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
#model.train(new_data)

print "####################################################################"
print "####################################################################"

print model.most_similar(positive = ['computer', 'skills'], negative = ['volunteers'], topn = 5)

print "####################################################################"
print "####################################################################"

print model.n_similarity(['king', 'queen'], ['monarch', 'rule'])