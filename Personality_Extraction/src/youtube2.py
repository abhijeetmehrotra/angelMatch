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

import pickle
from sklearn.externals import joblib
stop = set(stopwords.words('english'))
def preprocess_text(text):
    tokens = word_tokenize(text)
    cleanup = " ".join(filter(lambda word: word not in stop, text.split()))
    return cleanup
def linear_regression(Train_List_Unigrams, labels, regr, Test_List_Unigrams, testlabels,classifier_name):
    labels1 = normalize_vector(labels)
    regr.fit(np.array(Train_List_Unigrams.toarray()).astype(np.float), np.array(labels1).astype(np.float))
    joblib.dump(regr, classifier_name+'.pkl')
    testlabels = np.array(testlabels).astype(np.float)

    Test_List_Unigrams = np.array(Test_List_Unigrams.toarray()).astype(np.float)
    testlabels = normalize_vector(testlabels)
    predicted = regr.predict(Test_List_Unigrams)
    #predicted = normalize_vector(predicted)
    print ('train unigrams', Train_List_Unigrams.shape[0])
    print ('test unigrams', Test_List_Unigrams.shape[0])


    #predicted = normalize_vector(predicted)
    print("Mean squared error: %.2f"
          % np.mean((predicted - testlabels)**2 ))
    print("Mean abs error: %.2f"
          % np.mean(np.abs(predicted - testlabels) ))
    print('Variance score: %.2f' % np.std((predicted - testlabels) ** 2))
    '''
    for i in range(100):
       print (predicted[i] - testlabels[i])**2
    '''

def normalize_vector(vector):
   '''
    preprocessing.normalize()
    normalized_vector = np.array(vector).astype(np.float)
    std = np.std(normalized_vector)
    normalized_vector = (normalized_vector - np.mean(normalized_vector)) / np.max(normalized_vector)
    return normalized_vector
    '''
   #xmin = np.min(vector)
   #return (vector  / (np.max(vector)))

   return vector



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

combined_file = 'test_you.csv'
#personality_file = pd.read_csv(combined_file, delimiter=",")



testfile  = open(combined_file, "r")
#reader = pd.read_csv(combined_file, delimiter=",")
#ifile  = open('reviews_32618_for_1098_users_with_location.csv', "r")
reader = csv.reader(testfile, delimiter =',')

rownum = 0
test_review_text = []
test_user_text = []
labels1 = []
labels2 = []
labels3 = []
labels4 = []
labels5= []
senti=[]
rownum = 0
review_text= []
with open(combined_file, 'r') as f:
    data = [row for row in csv.reader(f.read().splitlines())]
print (len(data))
for row in data:
    #if(rownum == 1):
    #    break
    #print row
    if(rownum==0):

        print (row)
    else:
        colnum = 0
        for col in row:
            if(colnum==1):
                col = unicode(col, errors='ignore')
                col = preprocess_text(col)
                review_text.append(col)
            if(colnum == 2):
                labels1.append(float(col))
            if (colnum == 3):
                labels2.append(float(col))
            if (colnum == 4):
                labels3.append(float(col))
            if (colnum == 5):
                labels4.append(float(col))
            if (colnum == 6):
                labels5.append(float(col))
            if(colnum == 7):
                senti.append(10000*float(col))
            colnum= colnum + 1
    rownum = rownum +  1
#print (labels1)
testfile.close()

#print (review_text)
print ('review text', len(review_text))
print ('labels1', len(labels1))
#print(user_text)
#print (review_text)
LEN = 250
SPLITLEN = 200
test_review_textz = []
train_review_text = review_text[:SPLITLEN]
test_review_textz = review_text[SPLITLEN:]

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
trainsenti = senti[:SPLITLEN]
testsenti = senti[SPLITLEN:]
print ('senti size', len(senti))
print ('trainlabels', len(trainlabels1))
print ('test_labels', len(testlabels1))
print ('tran_Txt', len(train_review_text))
print ('test_Review_text', len(test_review_textz))

Unigrams_Count_Map = CountVectorizer( ngram_range=(1, 2) ,token_pattern=r'\b\w+\b',  max_df=0.99, min_df=0.01)
Train_List_Unigrams = Unigrams_Count_Map.fit_transform(train_review_text);
#Train_List_Unigrams = Train_List_Unigrams.toarray();
print (Train_List_Unigrams.shape)
print(len(trainsenti))
#trainsenti = np.asarray(trainsenti).reshape(Train_List_Unigrams.shape[0],1)

#print (trainsenti.shape)
#for i in range(100):
#    Train_List_Unigrams = np.hstack((Train_List_Unigrams, np.array(trainsenti).reshape(trainsenti.shape[0], 1)))

print (Train_List_Unigrams.shape)
regr = linear_model.LarsCV(max_n_alphas=4000)
#Train_List_Unigrams = bsr_matrix(Train_List_Unigrams)

Test_List_Unigrams = Unigrams_Count_Map.transform(test_review_textz);
#Test_List_Unigrams = Test_List_Unigrams.toarray();
#testsenti = np.asarray(testsenti).reshape(Test_List_Unigrams.shape[0],1)
#for i in range(100):
#    Test_List_Unigrams = np.hstack((Test_List_Unigrams, testsenti))
print ("tran shape", Train_List_Unigrams.shape)
print ("test shape", Test_List_Unigrams.shape)
#Train_List_Unigrams = bsr_matrix(Train_List_Unigrams)
#Test_List_Unigrams = bsr_matrix(Test_List_Unigrams)
linear_regression(Train_List_Unigrams, trainlabels1, regr,Test_List_Unigrams, testlabels1, 'one')
linear_regression(Train_List_Unigrams, trainlabels2, regr,Test_List_Unigrams, testlabels2, 'two')
linear_regression(Train_List_Unigrams, trainlabels3, regr,Test_List_Unigrams, testlabels3, 'third')
linear_regression(Train_List_Unigrams, trainlabels4, regr,Test_List_Unigrams, testlabels4, 'fourth')
linear_regression(Train_List_Unigrams, trainlabels5, regr,Test_List_Unigrams, testlabels5, 'five')