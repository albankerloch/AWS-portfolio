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
        add_annotation(params['Mail'], params['Nom'], params['Message'])

        # DynamoDB 'put_item' to add or update a note
        newNoteId = upsertItem(dynamoDBResource, ddbTable, params['Mail'], params['Nom'], params['Message'])

    except Exception as e:
        print(e)
        response['body'] = e
        return response
        
    response['statusCode'] = 200
    response['body'] = str(newNoteId)
    return response

def upsertItem(dynamoDBResource, ddbTable, Mail, Nom, Message):
    print('upsertItem Function')

    # set the table's name identifier
    table = dynamoDBResource.Table(ddbTable)
    
    # Put the item in the database, this will create a new item if the UserId and NoteId
    # do not match an existing note. If it does, it will update that note.
    table.put_item(
        Item={
            'Mail': Mail,
            'Timestamp': int(time.time()),
            'Nom': Nom,
            'Message': Message
        }
    )
    return Mail
    
def add_annotation(Mail, Nom, Message):
    print('add_annotation Function')
    xray_recorder.begin_subsegment('Add a contact')
    xray_recorder.put_annotation("Mail", Mail)
    xray_recorder.put_annotation("Nom", Nom)
    xray_recorder.put_annotation("Message", Message)
    xray_recorder.end_subsegment()



def extractParams(event):
    print('extractParams Function')
    print(event["body"])
    Mail = "MAIL TEST"
    Nom = "NOM TEST"
    Message = "MESSAGE TEST"
    
    return {
        'Mail': Mail,
        'Nom': Nom,
        'Message': Message
    }
