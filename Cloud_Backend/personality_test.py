from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
cons = joblib.load('cons.pkl')
agreableness = joblib.load('agreableness.pkl')

def normalize_vector(vector):
    return vector

def predict_agreableness(summary):
    summary = [summary]
    Unigrams_Count_Map = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', max_df=0.99, min_df=0.01)
    Test_List_Unigrams = Unigrams_Count_Map.transform(summary)
    Test_List_Unigrams = np.array(Test_List_Unigrams.toarray()).astype(np.float)
    #testlabels = normalize_vector(testlabels)
    #cons_predicted = cons.predict(Test_List_Unigrams)
    agreableness_predicted = agreableness.predict(Test_List_Unigrams)
    return agreableness


def predict_cons(summary):
    summary = [summary]
    Unigrams_Count_Map = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', max_df=0.99, min_df=0.01)
    Test_List_Unigrams = Unigrams_Count_Map.transform(summary)
    Test_List_Unigrams = np.array(Test_List_Unigrams.toarray()).astype(np.float)
    #testlabels = normalize_vector(testlabels)
    cons_predicted = cons.predict(Test_List_Unigrams)
    return cons_predicted



print (predict_agreableness('I am doing well'))