import boto3
import json

# Initialize the boto3 client for Lambda
lambda_client = boto3.client('lambda', region_name='us-east-1')  # replace 'us-west-1' with your region

function_name = 'chat_bot_continuer'
payload = {
    "chat_id":"926d7215-e0c0-43ed-b753-b5d597175f95",
    "message":"Lash Lift with Tint"
}

# function_name = "chat_bot_initializer"
# payload = {
#     "business_id":"1fc1c04f-8ab6-4bb0-abe1-6c5938df94e4",
#     "message":"I want to book new appointment"
# }

response = lambda_client.invoke(
    FunctionName=function_name,
    InvocationType='RequestResponse',  # can be 'Event' for async invocation
    Payload=json.dumps(payload)
)

response_payload = response['Payload'].read().decode('utf-8')
print(response_payload)
