import json
import math
import dateutil.parser
import datetime
import time
import os
import boto3
import requests
import urllib.parse
from requests_aws4auth import AWS4Auth

host = 'https://search-photos-co6iq4cnbuiqna5nscag3gkw2m.us-east-2.es.amazonaws.com'
index = 'album'
type = '_doc'
url = host + '/' + index + '/' + '/_search'
headers = {"Content-Type": "application/json"}
region = 'us-east-2'
lex = boto3.client('lexv2-runtime', region_name='us-east-1')
service = 'es'
credentials = boto3.Session().get_credentials()

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)


def lambda_handler(event, context):
    print('event : ', event)
    print('context', context)
    q1 = event["queryStringParameters"]['q']
    print("q1:", q1)
    
    labels = detect_labels(q1)
    print("labels", labels)

    img_paths = []
    if len(labels) != 0:
        img_paths = list(set(get_photo_path(labels)))

    if len(img_paths) == 0:
        return {
            'statusCode': 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            'body': json.dumps('No Results found')
        }
    else:
        return {
            'statusCode': 200,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': json.dumps(img_paths),
            'isBase64Encoded': False
        }


    
def detect_labels(query):
    response = lex.recognize_text(
        botId='P6UUUDDKC5',
        botAliasId='0RZZX6VL3Q',
        localeId="en_US",
        sessionId="1234567890",
        text=query
    )
    print("lex-response", response)

    labels = []
    
    if 'interpretations' in response:
        for interpretation in response['interpretations']:
            if 'intent' in interpretation:
                intent = interpretation['intent']
                if 'slots' in intent:
                    for slot_name, slot_details in intent['slots'].items():
                        if slot_details and 'value' in slot_details:
                            value_details = slot_details['value']
                            # Check if 'interpretedValue' is not None before appending
                            if 'interpretedValue' in value_details and value_details['interpretedValue']:
                                labels.append(value_details['interpretedValue'])
    
    if not labels:
        print(f"No photo collection for query: {query}")
    
    return labels


def get_photo_path(keys):
    resp = []
    for key in keys:
        if key:  # Simplified check for None or empty strings
            print(f"Processing key: {key}")
            query = {"query": {"match": {"labels": key}}, "fields": ["_id"], "_source": False}
            headers = {"Content-Type": "application/json"}
            try:
                r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
                r.raise_for_status()  # This will throw an error for HTTP error responses
                response_json = r.json()
                resp.append(response_json)
                print(f"Response for key '{key}': {response_json}")
            except requests.RequestException as e:
                print(f"Request failed for key '{key}': {e}")

    print("All responses: ", resp)
    
    output = []
    for r in resp:
        if 'hits' in r:
            for val in r['hits']['hits']:
                key = val['_id']
                if key not in output:
                    output.append(key)
                    print(f"Added document ID to output: {key}")

    print(f"Final output: {output}")
    return output
