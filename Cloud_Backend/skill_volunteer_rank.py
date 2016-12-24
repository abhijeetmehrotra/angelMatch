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

def generate_cause_similarity(user_causes, org_causes):
  return len(list(set(user_causes).intersection(set(org_causes))))
  
def add_skills(skills_set):
  global skillset
  for newskill in skills_set:
    newskill = newskill.replace(' ', '_').replace(',_', ',').lower().split(',')
    for skill in newskill:
      if (skill not in skillset):
        skillset.append(skill)

with open('demofile.json', 'r') as infile:
  user_data = json.load(infile)

with open('orgformat.json', 'r') as infile2:
  org_data = json.load(infile2)

causes = ["Women Empowerment","Child Education","LGBTQ","Veteran","Homeless Shelter","Substance Abuse","Animal Welfare"]

organization_skills = org_data['hits']['hits'][0]['_source']['skills']
organization_causes = org_data['hits']['hits'][0]['_source']['causes_supported']

orgskills = organization_skills
maxw = len(orgskills)

#read skills
skillset = list(pd.read_csv("skills.csv", delimiter=","))
count = 0
for skills in skillset:
  val = skills.replace(' ', '_').lower()
  skillset[count] = val
  count = count + 1

for user in user_data['hits']:
  add_skills(user['_source']['skills'])

add_skills(orgskills)
       
#create word2vec
w2v2_dataset = []
dataset_of_datasets = []

for val in skillset:
    w2v2_dataset.append(val.replace(' ', '_').replace(',_', ',').lower())

dataset_of_datasets.append(w2v2_dataset)
w2v2 = Word2Vec(dataset_of_datasets, min_count = 1)

orgskills = orgskills[0].encode('ascii').replace(' ', '_').replace(',_', ',').lower().split(',')
organization_causes = organization_causes[0].encode('ascii').replace(' ', '_').replace(',_', ',').lower().split(',')

#prediction
ranked_dict = dict()
for user in user_data['hits']:
  id_ = user['_id']
  skills = [user['_source']['skills'][0].encode('ascii')][0].replace(' ', '_').replace(',_', ',').lower().split(',')
  skill_sim = w2v2.n_similarity(skills, orgskills)
  user_supported_causes = [user['_source']['causes_supported'][0].encode('ascii')][0].replace(' ', '_').replace(',_', ',').lower().split(',')
  cause_sim = generate_cause_similarity(user_supported_causes, organization_causes)
  sim = (cause_sim*3 + skill_sim*2)/5.0
  ranked_dict[id_] = sim

with open('ranked_lists.txt', 'w') as outfile:
  json.dump(ranked_dict, outfile)