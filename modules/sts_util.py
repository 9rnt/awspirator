import boto3

def get_session(log, profile=None, role_arn=None, external_id=None, region='us-west-2',session_name='awxotic_session'):
    '''
    Get IAM Role to perform the actions
    '''
    log.debug(f'[aws_session] Start with the profile: {profile}')
    if profile:
        session = boto3.Session(profile_name=profile,region_name=region)
        client = session.client('sts')
        if role_arn and external_id:        
            response = client.assume_role(RoleArn=role_arn, ExternalId=external_id, RoleSessionName=session_name)
            session = boto3.Session(
                aws_access_key_id=response['Credentials']['AccessKeyId'],
                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                aws_session_token=response['Credentials']['SessionToken'])
            log.info(f'[awsSession] Successfully assumed the role {role_arn}')
            return session
        elif role_arn:
            response = client.assume_role(RoleArn=role_arn, RoleSessionName=session_name)
            log.info("Assumed role: %s", response)
            session = boto3.Session(
                aws_access_key_id=response['Credentials']['AccessKeyId'],
                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                aws_session_token=response['Credentials']['SessionToken'])
            log.info(f'[awsSession] Successfully assumed the role {role_arn}')
            return session
        else:
            log.info(f'[aws_session] No new role was detected. Continue with Service IAM role')
            return session
    else:
        return boto3.Session(region_name=region)
