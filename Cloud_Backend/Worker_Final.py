from watson_developer_cloud import AlchemyLanguageV1
import json
import clustering_cosine_clustering, clustering_cosine_clustering2
import boto3
import boto
from boto import sns
from concurrent.futures import ThreadPoolExecutor
import time
REGION = 'us-east-1'
TOPIC  = 'arn:aws:sns:us-east-1:207910673185:tweets'
URL    = 'www.googhfdhdle.com'
aws_access_key_id = 'AKIAIROYLKHSWD62VNOA'
aws_secret_access_key = '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'

#conn = boto.sns.connect_to_region( REGION )

#pub = conn.publish(topic=TOPIC, message=URL)
queueName = 'angelpush'
# alchemy_language = AlchemyLanguageV1(api_key='a505cc1904981e440eb6c34fd3ff4d11fe0715fa')


sqs = boto3.resource('sqs',aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key, region_name  = REGION)
print (sqs)
queue = sqs.get_queue_by_name(QueueName=queueName)
print (queue)
'''
arn = '	arn:aws:sqs:us-east-1:207910673185:tweets'       # enter your SNS ARN here
sns = boto3.resource('sns')
platform_endpoint = sns.PlatformEndpoint(arn)
'''

def process_tweets():
	exit()
	for message in queue.receive_messages(MessageAttributeNames=['All']):
		print('message...........')
		print(message.get_body())
		if message.message_attributes is not None:
			print (message)
		message.delete()

def main():
    #process_tweets()
    executor = ThreadPoolExecutor(max_workers=1)
    while True:
        executor.submit(process_tweets)

if __name__ == '__main__':
    #main()
	print ('hey')
import boto3
import json

region_name = 'us-east-1'
queue_name = 'tweets'
max_queue_messages = 10
message_bodies = []
aws_access_key_id = 'AKIAIROYLKHSWD62VNOA'
aws_secret_access_key = '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'
'''
sqs = boto3.resource('sqs', region_name=region_name,  aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
'''
#queue = sqs.get_queue_by_name(QueueName=queue_name)
while True:
    messages_to_delete = []
    for message in queue.receive_messages(MaxNumberOfMessages=1):
		print (message.body)
		import urllib2
		org_dict=dict()
		message_split = message.body.split(',')
		org_skills = message_split[0].split('|')
		org_dict['skills'] = org_skills

		org_causes = message_split[1].split('|')
		org_dict['issues_supported'] = org_causes
		print (org_causes)
		print (org_skills)
		org_html = json.dumps(org_dict, ensure_ascii=True)
		open('org_skills.txt', 'w').write(org_html)
		response = urllib2.urlopen(message_split[-1])
		html = response.read()
		print (type(html))
		#print (html)
		body='json failed in this case'
		required_object = json.loads(html)['hits']
		persons_dict = dict()
		persons_dict['person'] = []
		#print (required_object)

		for person in required_object:
			persons_dict['person'].append(person['_source'])
			#print person['_source']
		print (persons_dict)
		html = (persons_dict)
		try:
			html = json.dumps(persons_dict, ensure_ascii=True)
			open("person_json.json",'w').write((html))
			clustering_cosine_clustering2.solve()
		except:
			print ('except')
		#message_bodies.append(body)
		#print (body)
		messages_to_delete.append({
            'Id': message.message_id,
            'ReceiptHandle': message.receipt_handle
        })

    # if you don't receive any notifications the
    # messages_to_delete list will be empty
    if len(messages_to_delete) == 0:
        print('hey')
    # delete messages to remove them from SQS queue
    # handle any errors
    else:
        delete_response = queue.delete_messages(
                Entries=messages_to_delete)
#print message_bodies
