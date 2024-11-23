import boto3
import requests
import json

# Initialize AWS clients
iam = boto3.client('iam')
secrets_client = boto3.client('secretsmanager')

# Function to retrieve secrets from Secrets Manager
def get_secret():
    secret_name = "gitlab-key-rotation-secrets"  # Replace with your actual secret name
    response = secrets_client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    return secret

# Main function to rotate AWS access keys
def rotate_aws_keys(event, context):
    # Retrieve GitLab secrets from Secrets Manager
    secrets = get_secret()
    GITLAB_TOKEN = secrets['GITLAB_TOKEN']
    GITLAB_GROUP_ID = secrets['GITLAB_GROUP_ID']
    AWS_IAM_USER = secrets['AWS_IAM_USER']

    # Step 1: Create a new access key for the IAM user
    new_key = iam.create_access_key(UserName=AWS_IAM_USER)['AccessKey']
    new_access_key = new_key['AccessKeyId']
    new_secret_key = new_key['SecretAccessKey']
    print("New AWS Access Key Created.")

    # Step 2: Update GitLab group-level variables with the new access key
    gitlab_api_url = f"https://gitlab.com/api/v4/groups/{GITLAB_GROUP_ID}/variables"

    # Update AWS_ACCESS_KEY_ID in GitLab group variables
    requests.put(
        f"{gitlab_api_url}/AWS_ACCESS_KEY_ID",
        headers={'PRIVATE-TOKEN': GITLAB_TOKEN},
        data={'value': new_access_key}
    )

    # Update AWS_SECRET_ACCESS_KEY in GitLab group variables
    requests.put(
        f"{gitlab_api_url}/AWS_SECRET_ACCESS_KEY",
        headers={'PRIVATE-TOKEN': GITLAB_TOKEN},
        data={'value': new_secret_key}
    )
    print("Updated GitLab group-level variables with new AWS keys.")

    # Step 3: List existing keys and delete the old key
    access_keys = iam.list_access_keys(UserName=AWS_IAM_USER)['AccessKeyMetadata']
    for key in access_keys:
        if key['AccessKeyId'] != new_access_key:
            iam.update_access_key(
                UserName=AWS_IAM_USER,
                AccessKeyId=key['AccessKeyId'],
                Status='Inactive'
            )
            iam.delete_access_key(UserName=AWS_IAM_USER, AccessKeyId=key['AccessKeyId'])
            print(f"Old AWS Access Key {key['AccessKeyId']} has been deleted.")

# Entry point for AWS Lambda
def lambda_handler(event, context):
    rotate_aws_keys(event, context)
