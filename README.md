# AWSpirator

A Python utility for retrieving secrets from AWS Secrets Manager and Parameter Store across all regions.

## Features

- Retrieves secrets from AWS Secrets Manager across all available regions
- Retrieves secure strings from AWS Systems Manager Parameter Store across all regions
- Handles pagination for large sets of secrets
- Provides detailed logging for tracking retrieval progress and potential issues
- Supports error handling for insufficient permissions
- Flexible output formats (JSON, CSV, or console output)
- Support for AWS profiles and role assumption

## Prerequisites

- Python 3.x
- AWS credentials configured (either through AWS CLI, environment variables, or IAM role)
- Required Python packages:
  - boto3
  - botocore

## Installation
```bash
git clone https://github.com/yourusername/awspirator.git
cd awspirator
pip install -r requirements.txt
```
## CLI Usage
```bash
python cli.py [options]
```
### Options

- `--profile`: Specify the AWS profile (default is 'default')
- `--role-arn`: Specify the AWS role to be assumed
- `--external-id`: Specify the external ID for role assumption
- `--parameter-store`: Include Parameter Store secrets in addition to Secrets Manager
- `--output`: Specify output format (csv, json)
- `--file-path`: Specify the path for the output file
- `-v, --verbose`: Increase verbosity level (can be used multiple times)
  - `-v`: WARN level
  - `-vv`: INFO level
  - `-vvv`: DEBUG level

### Examples

```bash
python cli.py --profile myprofile --role-arn arn:aws:iam::123456789012:role/MyRole --external-id 1234567890 --parameter-store --output csv --file-path secrets.csv -vvv
```

## Required AWS Permissions

- `secretsmanager:GetSecretValue`
- `ssm:GetParameter`
- `ssm:GetParameterHistory`
- `sts:AssumeRole`
- `sts:GetCallerIdentity`

## License

This project is licensed under the MIT License - see the LICENSE file for details.