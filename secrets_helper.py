import json

import boto3
from botocore.exceptions import ClientError


def get_secrets(prefix, region_name='us-east-1', secret_name='prod/v1/chrone'):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secrets = get_secret_value_response['SecretString']
    secrets_json = json.loads(secrets)
    response = {}
    for key in secrets_json:
        if key.startswith(prefix):
            response[key] = secrets_json[key]

    return response
