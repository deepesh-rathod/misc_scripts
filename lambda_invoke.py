import boto3
import json

region = 'us-east-1'
lambda_client = boto3.client('lambda', region_name=region)

function_name = 'initialize_chat'

response = lambda_client.invoke(
    FunctionName=function_name,
    InvocationType='RequestResponse',
)

response_payload = json.loads(response['Payload'].read().decode('utf-8'))

print(response_payload)

