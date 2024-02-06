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

services = pd.read_csv("table-data (7).csv",na_values="",index_col=False)
services = services.fillna("")
services.rename(columns = {'website category':'category'}, inplace = True)
services.rename(columns = {'service':'name'}, inplace = True)
srvcs = services.to_dict('records')
# srvc_str = json.dumps(srvcs)
# srvc_str = srvc_str.replace("'","''")
# timestamp = datetime.now().isoformat()
# insert_q = f"Insert into gbp_services_user values ('ChIJf7Bnhh4LK4cRwGvRpPPKT7A','False','{timestamp}','{srvc_str}')"
# sql_query(insert_q)
# update_q = f"update gbp_services_user set services='{srvc_str}' where place_id='ChIJL1wNMU-fj4ARzML8e5Pgdy4'"
# sql_query(update_q)
# conn.commit()
# print(0)

# place_id = "ChIJ68nmKvMTK4cRhZX6Mgu4ftw"
# query = f"Select services from gbp_services_user where place_id='{place_id}'"
# sql_query(query)
# res = cur.fetchall()
# services = res[0][0]

place_id = "ChIJL1wNMU-fj4ARzML8e5Pgdy4"
services_cats = []
for srvc in srvcs:
    if srvc['category'] not in services_cats:
        services_cats.append(srvc['category'])

website_services = []
for cat in services_cats:
    data = {
        "category":cat,
        "services":[]
    }
    for srvc in srvcs:
        if srvc['category'] == cat:
            data['services'].append({
                "name":srvc['name'],
                "price":srvc['price'],
                "description":srvc['description']
                })
    website_services.append(data)
website_services=json.dumps(website_services)
website_services=website_services.replace("'","''")
# update_q = f"update gmb_website_details set services='{website_services}' where place_id='{place_id}'"
# sql_query(update_q)
# conn.commit()
print("done")