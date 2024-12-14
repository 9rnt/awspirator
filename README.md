# AWSpirator

A Python utility for retrieving secrets from AWS Secrets Manager and Parameter Store across all regions.

## Features

- Retrieves secrets from AWS Secrets Manager across all available regions
- Retrieves secure strings from AWS Systems Manager Parameter Store across all regions
- Handles pagination for large sets of secrets
- Provides detailed logging for tracking retrieval progress and potential issues
- Supports error handling for insufficient permissions

## Prerequisites

- Python 3.x
- AWS credentials configured (either through AWS CLI, environment variables, or IAM role)
- Required Python packages:
  - boto3
  - botocore

## Required Permissions

The following AWS IAM permissions are needed:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeRegions",
                "secretsmanager:ListSecrets",
                "secretsmanager:GetSecretValue",
                "ssm:GetParametersByPath",
                "ssm:GetParameters"
            ],
            "Resource": "*"
        }
    ]
}
```

## Usage

```python
import boto3
import logging
from modules.secret_util import retrieve_secrets, retrieve_secrets_from_all_regions

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Create AWS session
session = boto3.Session()

# Retrieve secrets from AWS Secrets Manager
secrets_manager_secrets = retrieve_secrets(log, session)

# Retrieve secrets from Parameter Store
parameter_store_secrets = retrieve_secrets_from_all_regions(log, session)

# Combine all secrets
all_secrets = secrets_manager_secrets + parameter_store_secrets
```

## Output Format

The tool returns a list of dictionaries containing secret information:

### Secrets Manager Format
```python
{
    "ARN": "arn:aws:secretsmanager:region:account:secret:name",
    "Name": "secret-name",
    "SecretString": "secret-value",
    "Type": "SecretsManagerSecretString"
}
```

### Parameter Store Format
```python
{
    "ARN": "arn:aws:ssm:region:account:parameter/name",
    "Name": "/parameter/name",
    "SecretString": "parameter-value",
    "Type": "ParameterStoreSecureString"
}
```

## Error Handling

- The tool provides detailed logging for tracking progress and issues
- Failed secret retrievals are logged but don't stop the overall process
- Permission-related issues are handled gracefully with appropriate logging
