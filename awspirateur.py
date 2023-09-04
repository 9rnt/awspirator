from modules.secret_util import retrieve_secrets

def awspirateur(log,session):
    log.debug(f'[awsoirateur] Start')
    return retrieve_secrets(log,session)