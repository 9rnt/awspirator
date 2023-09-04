# awspirator
Simple script to collect all readable AWS secrets in secret manager from an AWS account

usage: cli.py [-h] [--profile PROFILE] [--role-arn ROLE_ARN] [--external-id EXTERNAL_ID] [--output OUTPUT] [--file-path FILE_PATH] [--verbose]
options:
  -h, --help            show this help message and exit
  --profile PROFILE     Specify the aws profile (default is default)
  --role-arn ROLE_ARN   Specify the aws role to be assumed
  --external-id EXTERNAL_ID
                        Specify the aws role to be assumed
  --output OUTPUT       Specify the output type csv, json
  --file-path FILE_PATH
                        Specify the path for the file to store the secrets
  --verbose, -v
