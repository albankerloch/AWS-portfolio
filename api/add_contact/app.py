# PollyNotes-CreateUpdateFunction
# This function allows us to create and update items in DynamoDB
#
# This lambda function is integrated with the following API method:
# /contact POST (create or update a note)

from __future__ import print_function
import boto3
import os
import time

dynamoDBResource = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    # Log debug information
    print(event)
    
    # Extracting the user parameters from the event
    Mail = event["Mail"]
    Nom = event["Nom"]
    Message = event['Message']
    ddbTable = os.environ['TABLE_NAME']
    
    # DynamoDB 'put_item' to add or update a note
    newNoteId = upsertItem(dynamoDBResource, ddbTable, Mail, Nom, Message)

    return newNoteId

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