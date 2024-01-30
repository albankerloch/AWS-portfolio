import boto3
import botocore
import json
import configparser
import os

def main(s3Client):
    print('Starting create website function...\n')

    print('Reading configuration file for bucket name...')
    config = readConfig()
    bucket_name = config['bucket_name']
    
    # Upload html files
    print('Uploading files for the website...')
    uploadWebsiteFiles(s3Client, bucket_name)

    print('\nEnd create website function...')


def uploadWebsiteFiles(s3Client, bucket):
    for root, subdirs, files in os.walk("api"):
        for filename in files:
            file_path = os.path.join(root, filename)[4:]
            print(file_path)
            s3Client.upload_file(
                Filename='api/' + file_path,
                Bucket=bucket,
                Key=file_path,
                ExtraArgs={
                    'ContentType': extract_content(file_path)
                }
            )

def extract_content(file_path):
    extension = file_path[file_path.rfind('.')+1:]
    match extension:
        case 'html':
            return 'text/html'
        case 'css':
            return 'text/css'
        case 'js':
            return 'text/js'
        case 'json':
            return 'text/json'
        case 'md':
            return 'text/md'
        case 'scss':
            return 'text/scss'
        case 'jpeg':
            return 'image/jpeg'
        case 'png':
            return 'image/png'
        case 'svg':
            return 'image/svg+xml'
        case _:
            return "text/plain"

def readConfig():
    config = configparser.ConfigParser()
    config.read('./config.ini')

    return config['S3']


# Create an S3 client to interact with the service and pass
# it to the main function that will create the buckets
client = boto3.client('s3')
try:
    main(client)
except botocore.exceptions.ClientError as err:
    print(err.response['Error']['Message'])
except botocore.exceptions.ParamValidationError as error:
    print(error)
