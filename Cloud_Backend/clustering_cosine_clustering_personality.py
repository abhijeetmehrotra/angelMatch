import simplejson
import csv
import numpy as np
skill_dict = dict()

default_skill_weight = 0

import csv
import json
import sys

person_data_file = open('new_persondata.json','w')
person_data_file.write('{')
begin = True
records = 0

person_data_file.write("\"person\":[")
for row in csv.DictReader(open('new_persondata.csv')):
    #if(records>=1):
    #    break
    records = records + 1
    if (not begin):
        person_data_file.write(',')
    if (begin):
        begin = False
    json.dump(row, person_data_file)
    print (row)
person_data_file.write(']')
person_data_file.write('}')
person_data_file.close()

def preprocess_skill(skill):
    skill = skill.lower().strip()
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
    organization_required_skills_vector = np.zeros(len(skill_dict) + 2)
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
        print ('organization skill found....', skill)
        organization_required_skills_vector[skill_dict[skill]] = skill_weight
    organization_required_skills_vector = organization_required_skills_vector/np.linalg.norm(organization_required_skills_vector)
    #print (organization_required_skills_vector)

skill_vector_dict = dict()
user_score_dict = dict()
user_vector_dict = []
with open('person_json.json') as json_data:
    #print (json_data)
    txt = open('person_json.json').read()
    #print ('.yield .........................')
    #print ('text\n' , txt)
    d = simplejson.loads(txt)
    #encoded_str = d.encode("utf8")
    #print (type(d))
    #print(d)
    person_list = d['person']
    for person in person_list:
        skill_vector = np.zeros(len(skill_dict) + 2)
        #print (person['skills'])
        #print (person['skills'])
        skills = person['skills'][0].split(',')
        #print (skills)
        endorsements = person['endorsements'][0].split(',')
        #print (endorsements)
        endorsements = endorsements
        connections = int(person['num_connections'])
        experience = int(person["volunteer_experience"])
        #print(endorsements)
        #print('skills.........',skills)
        for skill,endorsement_count in zip(skills, endorsements):
            skill = preprocess_skill(skill)
            #print ('candidates skill....',skill)
            if(not skill_dict.has_key(skill)):
                #;skill_dict[skill] = len(skill_dict)
                continue
            #print ('candidate skill found...' , skill)
            endorsement_count = int(endorsement_count)
            #print ('endorsements', endorsement_count)
            skill_vector[skill_dict[skill]] = endorsement_count  + default_skill_weight #+ skill_dict[skill]
        #print (skill_vector)
        skill_vector[-2] = experience
        skill_vector[-1] = connections
        user_vector_dict.append(skill_vector)
        skill_vector = skill_vector/ (np.linalg.norm(skill_vector)- 1e-8)
        #sprint ('skill_vector.....', skill_vector)
        score = np.dot(skill_vector, organization_required_skills_vector)
        #score=0
        print (score)
        user_score_dict[person['id']] = score

        #print (skill_vector)
        #print (person['endorsments'])
    #print (d['person'][0]['skills'])
    #print (d['person'][0]['endorsments'])
    #print (d['person'][1]['skills'])
    #print (d['person'][1]['endorsments'])
#print ('skill_dict', skill_dict)
all_skills_file = open('all_skills.json','w')
all_skills_file.write(str(skill_dict))
print (user_score_dict)

from sklearn.cluster import KMeans
X  = np.array(user_vector_dict)
kmeans = KMeans(n_clusters=1, random_state=0, tol=1e-8,algorithm='full')

kmeans.fit_transform(X)
open('final_vectors.txt','w').write(str(X))
open("final_label.txt",'w').write(str(kmeans.labels_))
open("cluster_centers.txt",'w').write(str(kmeans.cluster_centers_))
#kmeans.fit_predict(X[0])
'''
for label in kmeans.labels_:
    print (label)
    print ('\n')
'''
predictions_file = open('predictions.txt','w')#.write(str(kmeans.fit_predict(X)))

prediction_dict = dict()
for prediction in kmeans.fit_predict(X):
    predictions_file.write(str(prediction))
    if(not prediction_dict.has_key(str(prediction))):
        prediction_dict[str(prediction)] = 0
    prediction_dict[str(prediction)]  = prediction_dict[str(prediction)]  + 1
    predictions_file.write('\n')
#print (prediction_dict)

import boto3
region_name = 'us-east-1'
queue_name = 'tweets'
max_queue_messages = 10
message_bodies = []
aws_access_key_id = '<YOUR AWS ACCESS KEY ID>'
aws_secret_access_key = '<YOUR AWS SECRET ACCESS KEY>'
#sqs = boto3.resource('sqs', region_name=region_name)
sqs = boto3.resource('sqs', region_name = region_name)
queue = sqs.get_queue_by_name(QueueName='response')
print (queue)
# get_queue_url will return a dict e.g.
# {'QueueUrl':'......'}
# You cannot mix dict and string in print. Use the handy string formatter
# will fix the problem
print "Queue info : {}".format(queue)
message_send =str(user_score_dict)
responses = queue.send_message(queue, MessageBody= message_send)
# send_message() response will return dictionary
print "Message send response : {} ".format(responses)