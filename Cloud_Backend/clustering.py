import json

with open('sample.json') as json_data:

    d = json.load(json_data)
    #encoded_str = d.encode("utf8")
    #print (type(d))
    print(d)
    print (d['person'][0]['skills'])
    print (d['person'][0]['endorsments'])
    print (d['person'][1]['skills'])
    print (d['person'][1]['endorsments'])

import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
print (d)
plt.figure(figsize=(12, 12))

n_samples = 1500
random_state = 170
#X, y = make_blobs(n_samples=n_samples, random_state=random_state)
X = d['person']
y = 0
'''# Incorrect number of clusters
y_pred = KMeans(n_clusters=2, random_state=random_state).fit_predict(X)

plt.subplot(221)
plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.title("Incorrect Number of Blobs")
plt.show()'''
import gensim, logging, numpy

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = [d['person'][0]['skills'] + ['Python'] , d['person'][1]['skills']]

# train word2vec on the two sentences
#model = gensim.models.Word2Vec(sentences, min_count=1)
model = gensim.models.Word2Vec.load_word2vec_format('model.bin', binary=True)

#model.similarity(sentences[0], numpy.asarray(sentences[1]).transpose)
print (model.n_similarity(sentences[0], sentences[1]))

sentences = [d['person'][0]['endorsments'] + ['Python'] , d['person'][1]['endorsments']]
print (model.n_similarity(sentences[0], sentences[1]))