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
        log.error(f"[secret_util:get_network_interfaces] Unexpected error {e.response['Error']['Message']}")
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
        log.error(f"[secret_util:get_retrievable_secrets] Unexpected error {e.response['Error']['Message']}")
    
    return secrets


def retrieve_secrets(log,session):
    log.debug(f'[secret_util:retrieve_secrets] Start')
    secret_values=[]
    available_regions = get_available_regions(log,session)
    log.info(f'[secret_util:retrieve_secrets] Available regions: {available_regions}')
    for region in available_regions:
        log.info(f'[secret_util:retrieve_secrets] Looking for secrets in the region: {region}')
        client = session.client('secretsmanager',region)
        secrets_list=get_secrets(log,client)
    
        for secret in secrets_list:
            try:
                response = client.get_secret_value(
                    SecretId=secret.get('ARN')
                )
                secret_values.append({
                    "ARN":response.get('ARN'),
                    "Name":response.get('Name'),
                    "SecretString":response.get('SecretString')
                })
            except botocore.exceptions.ClientError as e :
                log.info(f"[secret_util:get_retrievable_secrets] Unexpected error {e.response['Error']['Message']}")
    return secret_values

        

