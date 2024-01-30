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
    
    # Chnage stack
    print('Changing Stack...')
    os.system('sam build --use-container --template api/template.yml')
    os.system('sam deploy --stack-name contact-api --s3-bucket ' + bucket_name)


    # Change api link in index.html
    idAPI = getIdAPI()
    print('Changing link to api ' + idAPI)
    os.system("sed -i 's/XXXXXXXXXX.execute-api.eu-west-3.amazonaws.com/" + idAPI + ".execute-api.eu-west-3.amazonaws.com/' portfolio/index.html")
    
    # Enable public access
    print('Enabling public access on the bucket...')
    enablePublicAccess(s3Client, bucket_name)

    # Upload html files
    print('Uploading files for the website...')
    uploadWebsiteFiles(s3Client, bucket_name)

    # Enable web hosting
    print('Enabling web hosting on the bucket...')
    enableWebHosting(s3Client, bucket_name)

    # Configure bucket policy
    print('Adding a bucket policy to allow traffic from the internet...')
    allowAccessFromWeb(s3Client, bucket_name)
    
    # Obtain the region from the boto3 session and print url
    session = boto3.session.Session()
    current_region = session.region_name
    print('\nYou can access the website at:\n')
    print('http://' + bucket_name + '.s3-website.' + current_region +'.amazonaws.com')
    
    # Change api link in index.html
    print('Revert API link to api ')
    os.system("sed -i 's/" + idAPI + ".execute-api.eu-west-3.amazonaws.com/XXXXXXXXXX.execute-api.eu-west-3.amazonaws.com/' portfolio/index.html")

    print('\nEnd create website function...')

def getIdAPI():
    clientAPI = boto3.client('apigateway')
    response = clientAPI.get_rest_apis()
    for item in response['items']:
        if item['name'] == 'contactAPISAM':
            return(item['id'])
    return('')


def uploadWebsiteFiles(s3Client, bucket):
    for root, subdirs, files in os.walk("portfolio"):
        for filename in files:
            file_path = os.path.join(root, filename)[10:]
            print(file_path)
            s3Client.upload_file(
                Filename='portfolio/' + file_path,
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
            
def enablePublicAccess(s3Client, bucket):
    # enable S3 web hosting using the objects you uploaded in the last method
    # as the index and error document for the website.
    s3Client.put_public_access_block(
        Bucket=bucket,
        PublicAccessBlockConfiguration={
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
    )
    
def enableWebHosting(s3Client, bucket):
    # enable S3 web hosting using the objects you uploaded in the last method
    # as the index and error document for the website.
    s3Client.put_bucket_website(
        Bucket=bucket,
        WebsiteConfiguration={
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'},
        }
    )


def allowAccessFromWeb(s3Client, bucket):
    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': "arn:aws:s3:::" + bucket + '/*'
        }]
    }
    bucket_policy = json.dumps(bucket_policy)

    # Apply the provided bucket policy to the website bucket
    # to allow your objects to be accessed from the internet.
    s3Client.put_bucket_policy(
        Bucket=bucket,
        Policy=bucket_policy
    )


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
