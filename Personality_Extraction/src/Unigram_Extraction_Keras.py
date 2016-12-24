    #ABHISHEK JINDAL
# RUN THIS FILE TO CREATE UNIGRAMS, BIGRAMS AND THE DATASET
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from nltk.corpus import stopwords
import csv, collections,re
from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from scipy import sparse, io
from scipy.sparse import *
import numpy as np
from sklearn import datasets, linear_model, preprocessing
import sys
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.datasets import imdb


stop = set(stopwords.words('english'))
def preprocess_text(text):
    tokens = word_tokenize(text)
    cleanup = " ".join(filter(lambda word: word not in stop, text.split()))
    return cleanup
def linear_regression(Train_List_Unigrams, labels, regr, Test_List_Unigrams, testlabels):
    labels1 = normalize_vector(labels)
    regr.fit(np.array(Train_List_Unigrams.toarray()).astype(np.float), np.array(labels).astype(np.float))
    testlabels = normalize_vector(testlabels)
    print (Train_List_Unigrams.shape[0])
    print (Test_List_Unigrams.shape[0])

    predicted = regr.predict(Test_List_Unigrams)
    predicted = normalize_vector(predicted)
    print("Mean squared error: %.2f"
          % np.mean((predicted - testlabels) ** 2))
    print('Variance score: %.2f' % np.std((predicted - testlabels) ** 2))
    '''
    for i in range(100):
       #print (predicted[i] - testlabels[i])**2
    '''

def normalize_vector(vector):
   '''
    preprocessing.normalize()
    normalized_vector = np.array(vector).astype(np.float)
    std = np.std(normalized_vector)
    normalized_vector = (normalized_vector - np.mean(normalized_vector)) / np.max(normalized_vector)
    return normalized_vector
    '''
   xmin = np.min(vector)
   return (vector - xmin) / (np.max(vector) - xmin)

pfile = open('pers_scores_1098.csv', "r")
preader = csv.reader(pfile)
user_score_dict = dict()
rownum = 0
for row in preader:
    # Save header row.

    if rownum == 0:
        header = row
        print header
    else:
        colnum = 0
        name = ''
        for col in row:
            #if(header[colnum])

            if(colnum == 0):
                name = col
                user_score_dict[col]=[]
            else:
                #print (header[colnum])
                user_score_dict[name].append(col)
            #print (header[colnum], col)

            #review_text.append(col)
            colnum += 1

    rownum += 1

pfile.close()

print (user_score_dict)
ifile  = open('reviews_32618_for_1098_users_with_location.csv', "r")
reader = csv.reader(ifile)

Reviews_Set = list(csv.reader(open('reviews_32618_for_1098_users_with_location.csv', 'r'), delimiter=','));


rownum = 0
review_text = []
user_text = []
labels1 = []
labels2 = []
labels3 = []
labels4 = []
labels5= []

for row in reader:
    # Save header row.

    if rownum == 0:
        header = row
        print header
    else:
        colnum = 0
        for col in row:
            #if(header[colnum])
            if(colnum == 1):
                user_text.append(col)
                labels1.append(float(user_score_dict[col][0]))
                labels2.append(float(user_score_dict[col][1]))
                labels3.append(float(user_score_dict[col][2]))
                labels4.append(float(user_score_dict[col][3]))
                labels5.append(float(user_score_dict[col][4]))
            if(colnum == 5):
                col = unicode(col, errors='ignore')
                col = preprocess_text(col)
                review_text.append(col)
            #print (header[colnum], col)

            #review_text.append(col)
            colnum += 1

    rownum += 1
#print (labels1)
ifile.close()


testfile  = open('testreviews.csv', "r")
reader = csv.reader(testfile)

rownum = 0
test_review_text = []
test_user_text = []
testlabels1 = []
testlabels2 = []
testlabels3 = []
testlabels4 = []
testlabels5= []

for row in reader:
    # Save header row.

    if rownum == 0:
        header = row
        print header
    else:
        colnum = 0
        for col in row:
            #if(header[colnum])
            if(colnum == 16):
                testlabels1.append(float(col))
            if(colnum == 17):
                testlabels2.append(float(col))
            if (colnum == 18):
                testlabels3.append(float(col))
            if (colnum == 19):
                testlabels4.append(float(col))
            if (colnum == 20):
                #print (header[colnum])
                testlabels5.append(float(col))
            if(colnum == 3):
                #print (col)
                col = unicode(col, errors='ignore')
                col = preprocess_text(col)
                test_review_text.append(col)
            #print (header[colnum], col)

            #review_text.append(col)
            colnum += 1

    rownum += 1
#print (labels1)
testfile.close()


#print (len(review_text))
#print(user_text)
#print (review_text)
LEN = 16310
SPLITLEN = 16310
'''
train_review_text = review_text[:SPLITLEN]
test_review_text = review_text[SPLITLEN:]

trainlabels1 = labels1[:SPLITLEN]
testlabels1 = labels1[SPLITLEN:]

trainlabels2 = labels2[:SPLITLEN]
testlabels2 = labels2[SPLITLEN:]

trainlabels3 = labels3[:SPLITLEN]
testlabels3 = labels3[SPLITLEN:]

trainlabels4 = labels4[:SPLITLEN]
testlabels4 = labels4[SPLITLEN:]

trainlabels5 = labels5[:SPLITLEN]
testlabels5 = labels5[SPLITLEN:]
print (len(trainlabels1))
print (len(testlabels1))
print (len(train_review_text))
print (len(test_review_text))
'''
Unigrams_Count_Map = CountVectorizer( ngram_range=(1, 2) ,token_pattern=r'\b\w+\b', min_df=0.01, max_df=0.99)
Train_List_Unigrams = Unigrams_Count_Map.fit_transform(review_text);
regr = linear_model.LinearRegression()
Test_List_Unigrams = Unigrams_Count_Map.transform(test_review_text);

'''
linear_regression(Train_List_Unigrams, labels1, regr,Test_List_Unigrams, testlabels1)
linear_regression(Train_List_Unigrams, labels2, regr,Test_List_Unigrams, testlabels2)
linear_regression(Train_List_Unigrams, labels3, regr,Test_List_Unigrams, testlabels3)
linear_regression(Train_List_Unigrams, labels4, regr,Test_List_Unigrams, testlabels4)
linear_regression(Train_List_Unigrams, labels5, regr,Test_List_Unigrams, testlabels5)
'''

Train_List_Unigrams = np.array(Train_List_Unigrams.toarray()).astype(np.float)
Test_List_Unigrams = np.array(Test_List_Unigrams.toarray()).astype(np.float)
print (Train_List_Unigrams.shape)
print (Test_List_Unigrams.shape)
maxlen = 80
X_train = sequence.pad_sequences(Train_List_Unigrams, maxlen=maxlen)
X_test = sequence.pad_sequences(Test_List_Unigrams, maxlen=maxlen)
print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)
#trainX = np.reshape(Train_List_Unigrams, (Train_List_Unigrams.shape[0], Train_List_Unigrams.shape[1], 1))
#testX = np.reshape(Test_List_Unigrams, (Test_List_Unigrams.shape[0], Test_List_Unigrams.shape[1], 1))
#trainX = np.reshape(Train_List_Unigrams, (Train_List_Unigrams.shape[0], 1, Train_List_Unigrams.shape[1]))
#testX = np.reshape(Test_List_Unigrams, (Test_List_Unigrams.shape[0], 1, Test_List_Unigrams.shape[1]))
# create and fit the LSTM network

max_features = 20000
print('Train...')
look_back = 3
model = Sequential()
model.add(Embedding(max_features, 128, dropout=0.2))
model.add(LSTM(128, dropout_W=0.2, dropout_U=0.2))  # try using a GRU instead, for fun
model.add(Dense(1))
model.add(Activation('sigmoid'))

# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print('Train...')
trainPredict = model.predict(X_train)
testPredict = model.predict(X_test)
testScore = math.sqrt(mean_squared_error(testlabels1[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))