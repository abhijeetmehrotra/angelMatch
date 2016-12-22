from flask import Flask, render_template, redirect, request, jsonify
from flask import make_response
from elasticsearch import Elasticsearch
import json, time, threading
from config import *

application = Flask(__name__)
keywordGlobal = ""

result = {
  "hits": [{
    "_index": "data",
    "_type": "volunteer",
    "_id": "AVknjU8yEWR49AZHhDB0",
    "_score": 1.0,
    "_source": {
      "uid": "1482427288907MIMBGvUU7h",
      "id": "MIMBGvUU7h",
      "fname": "Abhijeet",
      "lname": "Mehrotra",
      "email": "abhijeet.meh@gmail.com",
      "image_url": "null",
      "skills": [
        "Computer,Java"
      ],
      "endorsements": [
        "50,15"
      ],
      "volunteer_experience": 4,
      "num_connections": 340,
      "location": "New York City",
      "causes_supported": [
        "LBGTQ,Veteran"
      ],
      "industry": "Computer",
      "time_from": 679326360000,
      "time_to": 679330560000
    }
  },
  {
    "_index": "data",
    "_type": "volunteer",
    "_id": "AVknjU8yEWR49AZHhDB0",
    "_score": 1.0,
    "_source": {
      "uid": "1482427288907MIMBGvUU7h",
      "id": "MIMBGvUU7h",
      "fname": "Abhijeet",
      "lname": "Mehrotra",
      "email": "abhijeet.meh@gmail.com",
      "image_url": "null",
      "skills": [
        "Computer,Python"
      ],
      "endorsements": [
        "30,10"
      ],
      "volunteer_experience": 2,
      "num_connections": 120,
      "location": "New York",
      "causes_supported": [
        "LBGTQ,Old Age"
      ],
      "industry": "Computer",
      "time_from": 679326360000,
      "time_to": 679330560000
    }
  }
  ]
}

@application.route("/")
def home():
    #fetch the es instance
    es = getESInstance()

    #call es search without any keywords
    #result = es.search(size=5000,index='tweep')
    global result
    #return parsed result with rerender
    return render_template('final_template.html', result=parseRes(result))

@application.route('/keysearch', methods = ['GET','POST'])
def keysearch():
    #extracting the keywords from the search query
    keywords = request.form['search']
    
    #call es using keywords
    es = getESInstance()

    #update global keyword list
    updateKeywords(str(keywords))

    #call happens inside getMatchedTweets
    result = getMatchedTweets(es, str(keywords))

    #return parsed result with rerender
    return render_template('final_template.html', result=parseRes(result))

def getESInstance():
  #create and return new es instance based on host
  es = Elasticsearch([{'host':'search-tweetmap-4qeqqxxkmf62ajq6djhqwvlzni.us-east-1.es.amazonaws.com', 'port':443,'use_ssl':True}])
  return es

def getMatchedTweets(es, keyword):
    #extra check here for an empty keyword string inputed from form
    if len(keyword) is not 0:
      res = es.search(size=5000, index="tweep", body={"query": {"query_string": {"query": keyword}}})
    else:
      res = es.search(size=5000,index='tweep')

    #return result of es search with keywords  
    return res

def updateKeywords(keywordList):
  #update global keyword list
  global keywordGlobal
  keywordGlobal = keywordList

def parseRes(result):
  return result

# def parseRes(result):
#   #parsing results
#   for r in result['hits']['hits']:
#     #in each record, remove non-unicode chars from the tweet text (emoticons etc)
#     r['_source']['text'] = ''.join(i for i in r['_source']['text'] if ord(i)<128)
#   return result

@application.route('/rt', methods = ['GET','POST'])
def rt():
  #the real time tweet logic
  #fetching the es instance
  es = getESInstance()

  #retrieving global keywords
  global keywordGlobal

  #fetching based on keywords
  if len(keywordGlobal) is not 0:
    result = es.search(size=5000, index="tweep", body={"query": {"query_string": {"query": keywordGlobal}}})
  else:
    result = es.search(size=5000,index='tweep')
  
  #returning returnecd result without rerender
  return jsonify(parseRes(result))


@application.route('/geospatial', methods = ['GET','POST'])
def geospatial():
  #fetch latitude and longitude
  latitude = request.args.get('lat', 0, type=float)
  longitude = request.args.get('long', 0, type=float)
  
  es = getESInstance()
  global keywordGlobal
  return jsonify(1);
  
if __name__ == "__main__":
  try:
	  application.run()
  except:
    print('socket failure. Gracful exit. Please try again. Should work')
