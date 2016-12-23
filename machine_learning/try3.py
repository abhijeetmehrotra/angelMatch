#skill bag of words
#cluster according to skills
#find the cluster that the user belongs to
#distance metric to determine how far from skill a user is
from collections import defaultdict
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import time
from sklearn.ensemble import RandomForestClassifier
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
import numpy as np
import os

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

class KaggleWord2VecUtility(object):
    """KaggleWord2VecUtility is a utility class for processing raw HTML text into segments for further learning"""

    @staticmethod
    def review_to_wordlist( review, remove_stopwords=False ):
        # Function to convert a document to a sequence of words,
        # optionally removing stop words.  Returns a list of words.
        #
        # 1. Remove HTML
        review_text = BeautifulSoup(review).get_text()
        #
        # 2. Remove non-letters
        review_text = re.sub("[^a-zA-Z]"," ", review_text)
        #
        # 3. Convert words to lower case and split them
        words = review_text.lower().split()
        #
        # 4. Optionally remove stop words (false by default)
        if remove_stopwords:
            stops = set(stopwords.words("english"))
            words = [w for w in words if not w in stops]
        #
        # 5. Return a list of words
        return(words)

    # Define a function to split a review into parsed sentences
    @staticmethod
    def review_to_sentences( review, tokenizer, remove_stopwords=False ):
        # Function to split a review into parsed sentences. Returns a
        # list of sentences, where each sentence is a list of words
        #
        # 1. Use the NLTK tokenizer to split the paragraph into sentences
        raw_sentences = tokenizer.tokenize(review.decode('utf8').strip())
        #
        # 2. Loop over each sentence
        sentences = []
        for raw_sentence in raw_sentences:
            # If a sentence is empty, skip it
            if len(raw_sentence) > 0:
                # Otherwise, call review_to_wordlist to get a list of words
                sentences.append( KaggleWord2VecUtility.review_to_wordlist( raw_sentence, \
                  remove_stopwords ))
        #
        # Return the list of sentences (each sentence is a list of words,
        # so this returns a list of lists
        return sentences

# Define a function to create bags of centroids
#
def create_bag_of_centroids( wordlist, word_centroid_map ):
    #
    # The number of clusters is equal to the highest cluster index
    # in the word / centroid map
    num_centroids = max( word_centroid_map.values() ) + 1
    #
    # Pre-allocate the bag of centroids vector (for speed)
    bag_of_centroids = np.zeros( num_centroids, dtype="float32" )
    #
    # Loop over the words in the review. If the word is in the vocabulary,
    # find which cluster it belongs to, and increment that cluster count
    # by one
    for word in wordlist:
        if word in word_centroid_map:
            index = word_centroid_map[word]
            bag_of_centroids[index] += 1
    #
    # Return the "bag of centroids"
    return bag_of_centroids


if __name__ == '__main__':

    #model = Word2Vec.load("300features_40minwords_10context")
    skillset = pd.read_csv("skills.csv", delimiter=",")
    
    w2v2_dataset = []
    dataset_of_datasets = []
    
    for val in skillset:
      w2v2_dataset.append(val.lower())

    dataset_of_datasets.append(w2v2_dataset)
    #model = Word2Vec(dataset_of_datasets, min_count = 1)
    model = Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

    # ****** Run k-means on the word vectors and print a few clusters
    #

    start = time.time() # Start time

    # Set "k" (num_clusters) to be 1/5th of the vocabulary size, or an
    # average of 5 words per cluster
    word_vectors = model.syn0
    num_clusters = word_vectors.shape[0] / 5

    # Initalize a k-means object and use it to extract centroids
    print "Running K means"
    kmeans_clustering = KMeans( n_clusters = num_clusters )
    idx = kmeans_clustering.fit_predict( word_vectors )

    # Get the end time and print how long the process took
    end = time.time()
    elapsed = end - start
    print "Time taken for K Means clustering: ", elapsed, "seconds."


    # Create a Word / Index dictionary, mapping each vocabulary word to
    # a cluster number
    word_centroid_map = dict(zip( model.index2word, idx ))

    # Print the first ten clusters
    for cluster in xrange(0,10):
        #
        # Print the cluster number
        print "\nCluster %d" % cluster
        #
        # Find all of the words for that cluster number, and print them out
        words = []
        for i in xrange(0,len(word_centroid_map.values())):
            if( word_centroid_map.values()[i] == cluster ):
                words.append(word_centroid_map.keys()[i])
        print words




    # Create clean_train_reviews and clean_test_reviews as we did before
    #

    # Read data from files
    train = pd.read_csv( os.path.join(os.path.dirname(__file__), 'data', 'labeledTrainData.tsv'), header=0, delimiter="\t", quoting=3 )
    test = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'testData.tsv'), header=0, delimiter="\t", quoting=3 )


    print "Cleaning training reviews"
    clean_train_reviews = []
    for review in train["review"]:
        clean_train_reviews.append( KaggleWord2VecUtility.review_to_wordlist( review, \
            remove_stopwords=True ))

    print "Cleaning test reviews"
    clean_test_reviews = []
    for review in test["review"]:
        clean_test_reviews.append( KaggleWord2VecUtility.review_to_wordlist( review, \
            remove_stopwords=True ))


    # ****** Create bags of centroids
    #
    # Pre-allocate an array for the training set bags of centroids (for speed)
    train_centroids = np.zeros( (train["review"].size, num_clusters), \
        dtype="float32" )

    # Transform the training set reviews into bags of centroids
    counter = 0
    for review in clean_train_reviews:
        train_centroids[counter] = create_bag_of_centroids( review, \
            word_centroid_map )
        counter += 1

    # Repeat for test reviews
    test_centroids = np.zeros(( test["review"].size, num_clusters), \
        dtype="float32" )

    counter = 0
    for review in clean_test_reviews:
        test_centroids[counter] = create_bag_of_centroids( review, \
            word_centroid_map )
        counter += 1


    # ****** Fit a random forest and extract predictions
    #
    forest = RandomForestClassifier(n_estimators = 100)

    # Fitting the forest may take a few minutes
    print "Fitting a random forest to labeled training data..."
    forest = forest.fit(train_centroids,train["sentiment"])
    result = forest.predict(test_centroids)

    # Write the test results
    output = pd.DataFrame(data={"id":test["id"], "sentiment":result})
    output.to_csv("BagOfCentroids.csv", index=False, quoting=3)
    print "Wrote BagOfCentroids.csv"