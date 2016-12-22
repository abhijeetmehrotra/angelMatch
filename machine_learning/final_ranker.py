#skill bag of words
#cluster according to skills
#find the cluster that the user belongs to
#distance metric to determine how far from skill a user is
from collections import defaultdict
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
import json, csv
import operator

def add_skills(skills_set):
  global skillset
  for newskill in skills_set:
    newskill = newskill.replace(' ', '_').replace(',_', ',').lower().split(',')
    for skill in newskill:
      if (skill not in skillset):
        skillset.append(skill)

peopleArray = pd.read_csv('persondata.csv', delimiter=',')

max_size = len(peopleArray)

org = {
  "id": "12345678",
  "name": "XYZ",
  "location": "New York",
  "email": "abc@xyz.com",
  "issues_supported": "Child Abuse Prevention, Shelters for Homeless People",
  "event_name": "Teach MATLAB to Homeless people and children",
  "skills": "MATLAB,Computer Science,Python",
  "event_from_date": "1482602400000",
  "event_to_date": "1482620400000",
  "num_years_operation": "5"
}

orgskills = org["skills"]
orgskills = orgskills.replace(' ', '_').replace(',_', ',').lower().split(',')

maxw = len(orgskills)

#read skills
skillset = list(pd.read_csv("skills.csv", delimiter=","))
count = 0
for skills in skillset:
  val = skills.replace(' ', '_').lower()
  skillset[count] = val
  count = count + 1

add_skills(peopleArray.skills)
add_skills(orgskills)
       
#create word2vec
w2v2_dataset = []
dataset_of_datasets = []

for val in skillset:
    w2v2_dataset.append(val.replace(' ', '_').replace(',_', ',').lower())

dataset_of_datasets.append(w2v2_dataset)
w2v2 = Word2Vec(dataset_of_datasets, min_count = 1)

#prediction
unweighted_scores = []
for person_skills in peopleArray.skills:
    user_skills = person_skills.replace(' ', '_').replace(',_', ',').lower().split(',')
    unweighted_scores.append(w2v2.n_similarity(user_skills, orgskills))

ranked_dict = dict()
for unwtc2 in range(0,max_size):
  id_ = peopleArray.id[unwtc2]
  score = unweighted_scores[unwtc2]
  print str(id_) + " " + str(score)
  ranked_dict[id_] = score
  
with open('ranked_lists.txt', 'w') as outfile:
  json.dump(ranked_dict, outfile)