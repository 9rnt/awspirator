import boto3
import botocore

def get_available_regions(log,session,default_region='us-west-2'):
    log.debug(f'[secret_util:get_available_regions] Start')
    client=session.client('ec2',default_region)
    try:
        response = client.describe_regions().get('Regions')
        available_regions=[]
        for i in response:
            if not i.get('RegionName') in available_regions:
                available_regions.append(i.get('RegionName'))
        return available_regions

    except botocore.exceptions.ClientError as e :
        log.error(f"[secret_util:get_available_regions] Unexpected error {e.response['Error']['Message']}")
        return None

def get_secrets(log,client,token=None):
    log.debug(f'[secret_util:get_secrets] Start')
    secrets=[]
    try:
        if token:
            response=client.list_secrets(IncludePlannedDeletion=True,NextToken=token)
        else:
            response=client.list_secrets(IncludePlannedDeletion=True)
        secrets=response.get('SecretList')
        token=response.get('NextToken')
        if token:
            secrets+=get_secrets(log,client,token)
    except botocore.exceptions.ClientError as e :
        log.debug(f"[secret_util:get_retrievable_secrets] Unexpected error {e.response['Error']['Message']}")
    
    return secrets

def retrieve_secrets(log,session):
    log.debug(f'[secret_util:retrieve_secrets] Start')
    secret_values=[]
    available_regions = get_available_regions(log,session)
    log.debug(f'[secret_util:retrieve_secrets] Available regions: {available_regions}')
    total_secrets = 0
    for region in available_regions:
        log.debug(f'[secret_util:retrieve_secrets] Looking for secrets in the region: {region}')
        client = session.client('secretsmanager',region)
        secrets_list=get_secrets(log,client)
        if not secrets_list:
            log.debug(f"[secret_util:retrieve_secrets] No secrets found in the region: {region}.\n<!> This can be due to insufficient permissions or no secrets in the region.")
            continue
        log.debug(f'[secret_util:retrieve_secrets] Found {len(secrets_list)} secrets in the region: {region}')
        total_secrets += len(secrets_list)
        count = 0
        for secret in secrets_list:
            try:
                response = client.get_secret_value(
                    SecretId=secret.get('ARN')
                )
                secret_values.append({
                    "ARN":response.get('ARN'),
                    "Name":response.get('Name'),
                    "SecretString":response.get('SecretString'),
                    "Type": "SecretsManagerSecretString"
                })
                count+=1
            except botocore.exceptions.ClientError as e :
                log.debug(f"[secret_util:get_retrievable_secrets] Unexpected error {e.response['Error']['Message']}")
        log.debug(f'[secret_util:retrieve_secrets] Retrieved {count} out of {len(secrets_list)} secrets in the region: {region}')
    log.info(f'[secret_util:retrieve_secrets] Retrieved {len(secret_values)} secrets out of {total_secrets} secrets. \n<!> If number of secrets is not the same as the total number of secrets, it means that some secrets are not retrievable due to insufficient permissions.')
    return secret_values

def retrieve_parameter_store_secrets(log,session,region, next_token=None):
    log.debug(f'[secret_util:retrieve_parameter_store_secrets] Start')
    client = session.client('ssm',region)
    parameter_store_secrets=[]
    if next_token:
        response = client.get_parameters_by_path(
            Path='/',
            Recursive=True,
            WithDecryption=True,
            MaxResults=10,
            NextToken=next_token
        )
    else:
        response = client.get_parameters_by_path(
            Path='/',
            Recursive=True,
            WithDecryption=True,
            MaxResults=10
        )
    parameters=response.get('Parameters')
    for parameter in parameters:
        if parameter.get('Type')=='SecureString':
            parameter_store_secrets.append({
                "ARN": parameter.get('ARN'),
                "Name": parameter.get('Name'),
                "SecretString": parameter.get('Value'),
                "Type": "ParameterStoreSecureString"
            })
    if response.get('NextToken'):
        parameter_store_secrets+=retrieve_parameter_store_secrets(log,session,region,response.get('NextToken'))
    return parameter_store_secrets

def retrieve_secrets_from_all_regions(log,session):
    log.debug(f'[secret_util:retrieve_secrets_from_all_regions] Start')
    secrets=[]
    available_regions = get_available_regions(log,session)
    log.debug(f'[secret_util:retrieve_secrets_from_all_regions] Available regions: {available_regions}')
    for region in available_regions:
        log.debug(f'[secret_util:retrieve_secrets_from_all_regions] Looking for secrets in the region: {region}')
        secrets+=retrieve_parameter_store_secrets(log,session,region)
    return secrets