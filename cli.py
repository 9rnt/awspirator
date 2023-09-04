import logging
import argparse
from awspirateur import awspirateur
from modules.sts_util import get_session
from modules.output import write_to_json_file, write_dict_to_csv

def cli():
    # cli configuration
    logging.basicConfig(format="%(levelname)s: %(message)s")
    log = logging.getLogger()
    parser = argparse.ArgumentParser(description="Collects readable secrets from an AWS account.")
    parser.add_argument('--profile', dest='profile', help='Specify the aws profile (default is default)')
    parser.add_argument('--role-arn', dest='role_arn', help='Specify the aws role to be assumed')
    parser.add_argument('--external-id', dest='external_id', help='Specify the aws role to be assumed')
    parser.add_argument('--output', dest='output', help='Specify the output type csv, json')
    parser.add_argument('--file-path', dest='file_path', help='Specify the path for the file to store the secrets')
    parser.add_argument('--verbose', '-v', dest='verbose', action='count', default=0)
    args = parser.parse_args()


    # set verbose level
    if args.verbose>2:
        log.setLevel('DEBUG')
    elif args.verbose>1:
        log.setLevel('INFO')
    elif args.verbose>0:
        log.setLevel('WARN')
    else:
        log.setLevel('ERROR')

    # get an aws session
    session = get_session(log, args.profile, args.role_arn, args.external_id)
    data=awspirateur(log,session)


    if args.output=="json":
        write_to_json_file(args.file_path, data)
    elif args.output=="csv":
        write_dict_to_csv(args.file_path, data)
    else:
        print(data)

    
    

if __name__ == "__main__":
    cli()