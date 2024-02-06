import os
import json
import google.oauth2.credentials
import google_auth_oauthlib
import googleapiclient.discovery as gapd
from datetime import time

ENDPOINT="database-2.cvwhw7xmj43j.ap-south-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="ap-south-1b"
DBNAME="postgres"
PASS = "January2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

import psycopg2
import pandas as pd
from datetime import datetime,date,timedelta

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

def insert_sql(table, data):
    query = 'insert into ' + table + '('
    keys = list(data.keys())
    query += ', '.join(keys) + ') values ('
    itr = 0
    for key in keys:
        itr += 1
        val = data[key]
        if type(val) == str:
            query += "'" + val + "'"
        elif type(val) == dict:
            query += "'" + json.dumps(val) + "'"
        elif type(val) == int:
            query += str(val)
        elif type(val) == float:
            query += str(val)
        elif val is None:
            query += "''"
        if itr == len(keys):
            query += ')'
        else:
            query += ', '
    try:
        sql_query(query)
        conn.commit()
        return 'Success'
    except Exception as e:
        print(e)
        return str(e)

# phone_number_df = pd.read_csv('update_phone_numbers.csv')

# for i in range(phone_number_df.shape[0]):
#     data = phone_number_df.iloc[i]
#     number = [data['sms_number']]
#     number = json.dumps(number)
#     place_id = data['place_id']
#     update_sql = "update gmb_website_details set sms_number = '{number}' where place_id='{place_id}'".format(number=number, place_id=place_id)
#     sql_query(update_sql)
#     conn.commit()
#     print("done for : ",data['biz_name'])

# sql_q = 'Select biz_name,sms_number from gmb_website_details'
# sql_query(sql_q)
# data = cur.fetchall()
# all_data = []
# for d in data:
#     biz_name = d[0]
#     sms_numbers = json.loads(d[1])
#     for number in sms_numbers:
#         all_data.append({
#             "biz_name":biz_name,
#             "sms_number":number
#         })

# all_data_df = pd.DataFrame(all_data)
# all_data_df.to_csv('all_sms_numbers.csv', index=False)
# print(0)
domain = 'beauty-vixen'
sql_q = f"Select place_id, biz_name, booking_link, number,dead,sms_number from gmb_website_details where url='{domain}'"
sql_query(sql_q)
res = cur.fetchall()

place_id = res[0][0]
biz_name = res[0][1]
booking_link = res[0][2]
number = res[0][3]
dead = res[0][4]
sms_number = json.loads(res[0][5])
print(0)
