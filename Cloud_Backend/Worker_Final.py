from watson_developer_cloud import AlchemyLanguageV1
import json
import boto3
import boto
from boto import sns
from concurrent.futures import ThreadPoolExecutor
import time
REGION = 'us-east-1'
TOPIC  = 'arn:aws:sns:us-east-1:207910673185:tweets'
URL    = 'www.googhfdhdle.com'


conn = boto.sns.connect_to_region( REGION )

#pub = conn.publish(topic=TOPIC, message=URL)
queueName = 'tweets'
# alchemy_language = AlchemyLanguageV1(api_key='a505cc1904981e440eb6c34fd3ff4d11fe0715fa')


sqs = boto3.resource('sqs')
print (sqs)
queue = sqs.get_queue_by_name(QueueName=queueName)

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
aws_access_key_id = '<YOUR AWS ACCESS KEY ID>'
aws_secret_access_key = '<YOUR AWS SECRET ACCESS KEY>'
sqs = boto3.resource('sqs', region_name=region_name)
queue = sqs.get_queue_by_name(QueueName=queue_name)
while True:
    messages_to_delete = []
    for message in queue.receive_messages(MaxNumberOfMessages=max_queue_messages):
		print (message.body)
		import urllib2

		response = urllib2.urlopen(message.body)
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
        break
    # delete messages to remove them from SQS queue
    # handle any errors
    else:
        delete_response = queue.delete_messages(
                Entries=messages_to_delete)
#print message_bodies