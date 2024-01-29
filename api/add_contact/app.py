# PollyNotes-CreateUpdateFunction
# This function allows us to create and update items in DynamoDB
#
# This lambda function is integrated with the following API method:
# /contact POST (create or update a note)

from __future__ import print_function
import boto3
import os
import time
import logging
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
from urllib.parse import parse_qs

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()


dynamoDBResource = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    # Log debug information
    print(event)
    
    # create the response object, the error code is 500 unless manually set to a success
    response = {
        'isBase64Encoded': False,
        'statusCode': 500,
        'body': '',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    
    ddbTable = os.environ['TABLE_NAME']
    
    try:
        # Extracting the user parameters from the event and environment
        params = extractParams(event)

        # Add X-Ray annotations to the trace
        add_annotation(params)

        # DynamoDB 'put_item' to add or update a note
        newNoteId = upsertItem(dynamoDBResource, ddbTable, params)

    except Exception as e:
        print(e)
        response['body'] = e
        return response
        
    response['statusCode'] = 200
    response['body'] = str(newNoteId)
    return response

def upsertItem(dynamoDBResource, ddbTable, params):
    print('upsertItem Function')

    # set the table's name identifier
    table = dynamoDBResource.Table(ddbTable)
    
    # Put the item in the database, this will create a new item if the UserId and NoteId
    # do not match an existing note. If it does, it will update that note.
    table.put_item(
        Item={
            'email': params['email'],
            'timestamp': int(time.time()),
            'name': params['name'],
            'message': params['message']
        }
    )
    return params['email']
    
def add_annotation(params):
    print('add_annotation Function')
    xray_recorder.begin_subsegment('Add a contact')
    xray_recorder.put_annotation("email", params['email'])
    xray_recorder.put_annotation("name", params['name'])
    xray_recorder.put_annotation("message", params['message'])
    xray_recorder.end_subsegment()



def extractParams(event):
    print('extractParams Function')
    print(event["body"])
    result = parse_qs(event["body"])
    print(result)
    
    return {
        'email' : result['email'][0],
        'name' : result['name'][0],
        'message' : result['message'][0]
    }
