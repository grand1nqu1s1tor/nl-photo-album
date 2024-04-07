import json
import os
import time
import boto3
from datetime import datetime
import requests
from requests_aws4auth import AWS4Auth
import os

defaultRegion = os.environ['AWS_REGION']

region = 'us-east-2'
service = 'es'
credentials = boto3.Session().get_credentials()


awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, defaultRegion, service, session_token=credentials.token)

rekognition = boto3.client('rekognition', region_name=region)
client=boto3.client('s3', region_name=region)
host = 'https://search-photos-co6iq4cnbuiqna5nscag3gkw2m.us-east-2.es.amazonaws.com'
index = 'album'
type = '_doc'
url = host + '/' + index + '/' + type + '/'
headers = { "Content-Type": "application/json" }

def lambda_handler(event, context):
    records = event['Records']
    print(records)

    for record in records:
        s3object = record['s3']
        bucket = s3object['bucket']['name']
        objectKey = s3object['object']['key']
        print(f"s3object: {s3object}")
        print(f"Bucket: {bucket}")
        print(f"Object Key: {objectKey}")

        response = client.head_object(Bucket=bucket, Key=objectKey)
        metadata = response['Metadata']
        custom_labels = metadata.get('customlabels', '').split(',') if 'customlabels' in metadata else []
        

        print(f"Object Key: {objectKey}")
        print(response)
        print(f"custom labels : {custom_labels}")
        
        image = {
            'S3Object' : {
                'Bucket' : bucket,
                'Name' : objectKey
            }
        }
        response = rekognition.detect_labels(Image = image)
        print(response)
        
        rekognition_labels = [label['Name'] for label in response['Labels']]
        all_labels = list(set(rekognition_labels + custom_labels))
        

        timestamp = datetime.now().strftime('%Y-%d-%mT%H:%M:%S')
        esObject = {
            'objectKey' : objectKey,
            'bucket' : bucket,
            'createdTimesatamp' : timestamp,
            'labels' : all_labels
        }
        
        r = requests.put(url + objectKey, auth=awsauth, json=esObject, headers=headers)
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.text}")
        if r.status_code != 200 and r.status_code != 201:
            print(f"Failed to index document: {r.text}")

    return {
        'statusCode': 200,
        'body': json.dumps('Event trigger confirmed.')
    }

    