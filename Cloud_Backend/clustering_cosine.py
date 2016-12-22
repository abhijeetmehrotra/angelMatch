import json
import csv
import numpy as np
skill_dict = dict()

default_skill_weight = 1
def preprocess_skill(skill):
    skill = skill.lower()
    skill = skill.replace(" ", "_")
    #TODO tokenize
    return skill


def process_all_skills():
    with open('skills.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            for col in row:
                col = preprocess_skill(col)
                #print(col)
                if(skill_dict.has_key(col)):
                    continue
                skill_dict[col] = len(skill_dict)
                #print ('\n')
    #for row in spamreader:
        #print(', '.join(row))
#exit(0)
process_all_skills()
print (len(skill_dict))

skill_vector_size = len(skill_dict)

with open('org.json') as json_data:

    d = json.load(json_data)
    organization_required_skills = d['skills'].split(',')
    organization_required_skills_vector = np.zeros(len(skill_dict))
    skill_weight = 1
    skill_weight_decay = 0.8
    print (d)

    for skill in organization_required_skills:
        skill = preprocess_skill(skill)
        print (skill)
        skill_weight = skill_weight * skill_weight_decay
        #TODO make it exponentially decayed
        if(not skill_dict.has_key(skill)):
            continue
        print ('skill found....', skill)
        organization_required_skills_vector[skill_dict[skill]] = skill_weight
    organization_required_skills_vector = organization_required_skills_vector/np.linalg.norm(organization_required_skills_vector)
    print (organization_required_skills_vector)

skill_vector_dict = dict()
user_score_dict = dict()
with open('sample.json') as json_data:

    d = json.load(json_data)
    #encoded_str = d.encode("utf8")
    #print (type(d))
    print(d)
    person_list = d['person']
    for person in person_list:
        skill_vector = np.zeros(len(skill_dict))
        #print (person['skills'])
        skills = person['skills']
        endorsements = person['endorsments']
        for skill,endorsement_count in zip(skills, endorsements):
            skill = preprocess_skill(skill)
            if(not skill_dict.has_key(skill)):
                skill_dict[skill] = len(skill_dict)
                continue
            endorsement_count = int(endorsement_count)
            skill_vector[skill_dict[skill]] = endorsement_count + default_skill_weight
        #print (skill_vector)
        skill_vector = skill_vector/ np.linalg.norm(skill_vector)
        score = np.dot(skill_vector, organization_required_skills_vector)
        print (score)
        user_score_dict[person['id']] = score
        #print (skill_vector)
        #print (person['endorsments'])
    #print (d['person'][0]['skills'])
    #print (d['person'][0]['endorsments'])
    #print (d['person'][1]['skills'])
    #print (d['person'][1]['endorsments'])
print ('skill_dict', skill_dict)

print (user_score_dict)

