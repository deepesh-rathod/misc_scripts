ENDPOINT="db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="us-east-1c"
DBNAME="postgres"
PASS = "March2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

import json
import psycopg2
import pandas as pd
import googleapiclient.discovery as gapd
import google.oauth2.credentials

def sql():
    global conn, cur
    try:
        conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS)
        cur = conn.cursor()
    except Exception as e:
        print("ERROR",e)


def sql_query(query):
    global cur
    try:
        cur.execute(query)
    except:
        sql()
        cur.execute(query) 

# query = "Insert into sp_website_feedback (uid,text) values ('tuid','trial text to check returing clause') returning *"
update_query = """update sp_website_feedback set uid='bc8045d5-4ce7-4446-968f-7c780fcd89b5', text='This is the feedback added from api request. xjdjjs', media='[]', context='{"section": "banner"}', status='live', updated_at='2023-07-25 17:03:46.188148' where id=3 RETURNING *"""
sql()
sql_query(update_query)
conn.commit()
print(10)