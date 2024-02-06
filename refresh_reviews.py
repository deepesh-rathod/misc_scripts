import os
import json
import google.oauth2.credentials
import google_auth_oauthlib
import googleapiclient.discovery as gapd
from datetime import time, timedelta
import uuid
import requests
import re
import boto3


ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "postgres"
REGION = "us-east-1c"
DBNAME = "postgres"
PASS = "March2021"
SECRET = "04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c"

import psycopg2
import pandas as pd
from datetime import datetime, date, timedelta


def sql():
    global conn, cur
    try:
        conn = psycopg2.connect(
            host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS
        )
        cur = conn.cursor()
    except Exception as e:
        print("ERROR", e)


def sql_query(query):
    global cur
    try:
        cur.execute(query)
    except:
        sql()
        cur.execute(query)

sections_query = "select section_data,biz_name from gmb_website_details where sections::text ilike '%141%'"
sql_query(sections_query)
res = cur.fetchall()

def copy_s3_file_with_new_name(bucket_name, source_key, destination_key):
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Copy the file in S3
    s3.copy_object(
        Bucket=bucket_name,
        CopySource={'Bucket': bucket_name, 'Key': source_key},
        Key=destination_key
    )

bucket_name = 'chrone-sp-website'



for r in res:
        # print(r[3])
        biz_name = r[1]
        section_data = r[0]
        if len(section_data['working_hrs']['content']['media'])!=2:
            print(f"Image not present!\nBiz name = {biz_name}")
        else:
            for img_data in section_data['working_hrs']['content']['media']:
                if img_data['url']:
                    desktop_image_url = img_data['url'].replace(".webp","_new.webp")
                    mobile_image_url = img_data['url'].replace(".webp","_new_min.webp")
                    resp_desktop = requests.get(desktop_image_url)
                    resp_mobile = requests.get(mobile_image_url)
                    if resp_desktop.status_code!=200:
                        print(f"Desktop Image not present!\nBiz name = {biz_name}")
                    if resp_mobile.status_code!=200:
                        print(f"Mobile Image not present!\nBiz name = {biz_name}")
                        source_key = desktop_image_url.replace("https://d15e7bk5l2jbs8.cloudfront.net/","")
                        destination_key = desktop_image_url.replace("https://d15e7bk5l2jbs8.cloudfront.net/","").replace("new.webp","new_min.webp")
                        try:
                            copy_s3_file_with_new_name(bucket_name, source_key, destination_key)
                        except:
                            print(f"Working Hrs image not present in system!\nBiz name = {biz_name}")

                else:
                    print(f"Image not present!\nBiz name = {biz_name}")

            