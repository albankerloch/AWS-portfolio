# AWS Portfolio

An portfolio on AWS

Features :
- Use of AWS SDK in python to create a S3 bucket website
- Use of AWS modern architecture :
    - CloudFormation SAM template 
    - API Getway
    - Lamba function
    - DynamoDB Database
    - S3
    - CloudWatch
    - Xrays
    - Cloud9
    - IAM


## Installation

In a Cloud9 environment : 


```bash
git clone --recurse-submodules git@github.com:albankerloch/aws-portfolio.git
cd aws-portfolio
pip3 install boto3
python3 create_bucket.py
python3 create_s3_website.py
```

(Python >=3.10 and suitable permissions needed)

## Usage

Visit the website at : http://portfolio-alban-kerloch-bucket.s3-website.eu-west-3.amazonaws.com/index.html
(if your AWS region is Paris)

#### Author : Alban Kerloc'h
#### Category: Web, Devops
#### Tag: AWS
