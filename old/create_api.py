import boto3
from pprint import pprint

client = boto3.client('cloudformation')

stack_name = "api-contact"
change_set_name = stack_name + "-cs"

# Create change set
cs_response = client.create_change_set(
  StackName=stack_name,
  ChangeSetType="CREATE",
  TemplateURL="https://portfolio-alban-kerloch-bucket.s3.eu-west-3.amazonaws.com/template.yml",
  ChangeSetName=change_set_name
)

waiter = client.get_waiter('change_set_create_complete')

waiter.wait(
    ChangeSetName=change_set_name,
    StackName=stack_name,
    WaiterConfig={
        'Delay': 3,
        'MaxAttempts': 50
    }
)

desc_response = client.describe_change_set(
    ChangeSetName=change_set_name,
    StackName=stack_name,
)
print("describe_change_set response Changes:")
pprint(desc_response["Changes"], indent=4)

exec_response = client.execute_change_set(
    ChangeSetName=change_set_name,
    StackName=stack_name
)

print("execute_change_set Changes:")
pprint(exec_response, indent=4)