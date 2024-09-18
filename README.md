# Packer AMI Build and Deployment with GitLab CI/CD

This repository demonstrates how to build Amazon Machine Images (AMIs) using Packer and deploy them across multiple AWS accounts and regions using GitLab CI/CD pipelines.

## Step 1: Add AWS Credentials

1. Go to your GitLab project’s **CI/CD** settings.
2. Navigate to **Variables**.
3. Add your AWS credentials (Access Key ID and Secret Access Key) as environment variables.

![Add AWS Credentials](./doc)

## Step 2: Configure Accounts and Regions

1. Update your configuration files to include the AWS accounts and regions where you want to deploy the AMIs.
2. Customize the AWS regions and accounts according to your requirements.

![Configure Accounts and Regions](./DOC2)

## Step 3: Run the CI/CD Pipeline

1. Trigger the GitLab CI/CD pipeline.
2. The pipeline will build the AMIs using Packer and distribute them across the specified regions and accounts.
3. Note that the pipeline may take up to 15 minutes to complete the distribution process.

![Run CI/CD Pipeline](./doc3)

## Additional Information

- Ensure that your GitLab runners have the necessary permissions to access AWS resources.
- Review Packer and GitLab CI/CD documentation for more details on configuration and usage.
