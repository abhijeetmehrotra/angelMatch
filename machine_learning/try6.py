#skill bag of words
#cluster according to skills
#find the cluster that the user belongs to
#distance metric to determine how far from skill a user is
from collections import defaultdict
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
import json

def add_skills(skills_set):
  global skillset
  for newskill in skills_set:
    newskill = newskill.replace(' ', '_').replace(',_', ',').lower().split(',')
    for skill in newskill:
      if (skill not in skillset):
        print skill
        skillset.append(skill)

peopleArray = pd.read_csv('persondata.csv', delimiter=',')

org = {
  "name": "XYZ",
  "location": "New York",
  "issues_supported": "Child Abuse Prevention, Shelters for Homeless People",
  "event_name": "Teach MATLAB to Homeless people and children",
  "event_from_date": "1482602400000",
  "event_to_date": "1482620400000",
  "num_volunteers": "5",
  "skills": "MATLAB, Computer Science"
}

orgskills = org["skills"]
orgskills = orgskills.replace(' ', '_').replace(',_', ',').lower().split(',')

maxw = len(orgskills)

orgweights = []

for w in range(maxw+1, 0):
  orgweights.append(w)
  sumow = sumow + w
  w = w - 1

#read skills
skillset = list(pd.read_csv("skills.csv", delimiter=","))
count = 0
print len(skillset)
for skills in skillset:
  val = skills.replace(' ', '_').lower()
  skillset[count] = val
  count = count + 1

add_skills(peopleArray.skills)
add_skills(orgskills)
#create data set
# for newskill in peopleArray.skills:
#   newskill = newskill.replace(' ', '_').replace(',_', ',').lower().split(',')
#   for skill in newskill:
#     if (skill not in skillset):
#       print skill
#       skillset.append(skill)
       
#create word2vec
w2v2_dataset = []
dataset_of_datasets = []

for val in skillset:
    w2v2_dataset.append(val.replace(' ', '_').replace(',_', ',').lower())

dataset_of_datasets.append(w2v2_dataset)
w2v2 = Word2Vec(dataset_of_datasets, min_count = 1)

#prediction
unwted_score_list = []
for person_skills in peopleArray.skills:
    user_skills = person_skills.replace(' ', '_').replace(',_', ',').lower().split(',')
    unwted_score_list.append(w2v2.n_similarity(user_skills, orgskills))

print unwted_score_list

#incorporating weights


#write to csv


