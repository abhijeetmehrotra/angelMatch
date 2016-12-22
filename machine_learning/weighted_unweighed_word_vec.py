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
sumow = 0

for w in range(1, maxw+1):
  orgweights.append(maxw + 1 - w)
  sumow = sumow + w

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
uskills = defaultdict(list)
index = 0
unweighted_scores = []
for person_skills in peopleArray.skills:
    user_skills = person_skills.replace(' ', '_').replace(',_', ',').lower().split(',')
    unweighted_scores.append(w2v2.n_similarity(user_skills, orgskills))
    uskills[index].append(user_skills)
    index = index + 1

#print unweighted_scores

#incorporating weights
sumorg = 0
for orgiter in range(0, maxw):
    temp = w2v2[orgskills[orgiter]]*orgweights[orgiter]
    sumorg = sumorg + temp

sumorg = sumorg/np.sum(orgweights)
sad = []
for counter in range(0,10001):
  weights = str(peopleArray[counter:counter+1].endorsements)
  weights = weights.split('    ')[1:]
  weights = weights[0].replace(' ', '').split(',')
  weights_2 = []
  for iters in range(0, len(weights)-1):
    if ('\n' in weights[iters]):
      weights[iters] = weights[iters].split('\n')[0]
    weights_2.append(int(weights[iters]))

  total_weight = 0#np.sum(weights_2)
  track = 0
  sumsk = 0

  #print weights_2
  user_skills = uskills[counter][0]
  for sk in user_skills:
    if track < len(weights_2):
      wt = weights_2[track]
    else:
      wt = 1
    total_weight = total_weight + wt
    sk = wt*w2v2[str(sk)]
    sumsk = sumsk + sk
    track = track + 1
  
  sumsk = sumsk / total_weight
  sad.append(np.sum(np.abs(sumsk - sumorg)))
  #print "#####"

# print np.argmin(np.abs(unweighted_scores))
# print np.argmin(sad)

un_weighted_map = dict()
weighted_map = dict()

unwtc=0
for val in np.abs(unweighted_scores):
  un_weighted_map[unwtc] = val
  unwtc = unwtc + 1

wtc=0
for val in sad:
  weighted_map[wtc] = val
  wtc = wtc + 1

sorted_uwt = sorted(un_weighted_map.items(), key=operator.itemgetter(1))
sorted_wt = sorted(weighted_map.items(), key=operator.itemgetter(1))

print sorted_wt[9995:10000]
print sorted_uwt[9995:10000]

sorted_unweighted = np.sort(np.abs(unweighted_scores))
sorted_weighted = np.sort(sad)

#write to csv
with open('ranked_list.csv', 'wb') as csvfile:
  opwriter = csv.writer(csvfile)
  for k, v in sorted_weighted.items():
    opwriter.writerow([k,v])


