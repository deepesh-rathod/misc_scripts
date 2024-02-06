# import json
# import gspread
# from boto3.session import Session
from datetime import datetime


# def init_s3_client(BUCKET_NAME):
#     AWS_ACCESS_KEY = "AKIASQ6IOBTRNZ2TKNHO"
#     AWS_ACCESS_SECRET = "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"
#     SESSION = Session(aws_access_key_id=AWS_ACCESS_KEY,
#                       aws_secret_access_key=AWS_ACCESS_SECRET)
#     S3 = SESSION.resource('s3')
#     MY_BUCKET = S3.Bucket(BUCKET_NAME)

#     return MY_BUCKET


# def get_gspread_conn():
#     key_bucket = init_s3_client('timelyai-keys')
#     key_file_path = "google_sheets/timelyai-314916-d5fc948298de-gsheet-key.json"
#     for key_file in key_bucket.objects.filter(Prefix=key_file_path):
#         gsheet_api_cred = json.loads(key_file.get()['Body'].read())
#     # gsheet_api_cred = json.load(open('./gsheet_api_cred.json'))
#     gc = gspread.service_account_from_dict(gsheet_api_cred)
#     return gc

# def append_data_to_sheet(gc, spreadsheet_url, spreadsheet_name, data, dump=False, dump_sheet_name=None):
#     # Open the spreadsheet
#     sheet = gc.open_by_url(spreadsheet_url).worksheet(spreadsheet_name)

#     # Prepare the row to append
#     headers = sheet.row_values(1)
#     row = [data.get(header, '') for header in headers]

#     # Append the row
#     sheet.append_row(row)
#     if dump and dump_sheet_name!=None:
#         dump_sheet=gc.open_by_url(spreadsheet_url).worksheet(dump_sheet_name)
#         dump_row = [data.get(header, '') for header in headers]
#         dump_sheet.append_row(dump_row)


# # Example usage
# gc = get_gspread_conn()
# spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1JmHXryzxI-x5CFDHLZtZ31m8EQqizJSa2R2bO6LCnvA'
# spreadsheet_name = 'website_live'
# data = {"timestamp":datetime.now().isoformat(),"uid":"1fc1c04f-8ab6-4bb0-abe1-6c5938df94e4","status":"live"}


# append_data_to_sheet(gc, spreadsheet_url, spreadsheet_name, data,True,"dump")

# import boto3
# import json
# from datetime import datetime

# # # Initialize a boto3 client for Lambda
# lambda_client = boto3.client('lambda', region_name='us-east-1')

# function_name = 'upload_data_to_gsheet'
# event_data = {
#     "sheet_url":"https://docs.google.com/spreadsheets/d/1JmHXryzxI-x5CFDHLZtZ31m8EQqizJSa2R2bO6LCnvA",
#     "sheet_name":"website_live",
#     "update_data":{'timestamp': datetime.now().isoformat(), 'uid': '1fc1c04f-8ab6-4bb0-abe1-6c5938df94e4', 'status': 'live'},
#     "dump":True,
#     "dump_sheet_name":"dump"
# }

# # # Invoke the Lambda function
# response = lambda_client.invoke(
#     FunctionName=function_name,
#     InvocationType='Event',
#     Payload=json.dumps(event_data)
# )

# # # Print the response
# print(response['Payload'].read())
