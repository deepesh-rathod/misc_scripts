ENDPOINT="database-2.cvwhw7xmj43j.ap-south-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="ap-south-1b"
DBNAME="postgres"
PASS = "January2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

import pandas as pd
import psycopg2
import json

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

# place_ids = [""]

# for place_id in place_ids:
#     data_q = f"Select biz_name,website from gmb_profile_details where place_id='{place_id}'"
#     sql_query(data_q)
#     data = cur.fetchall()
#     url_q = f"Select url from gmb_website_details where place_id='{place_id}'"
#     sql_query(url_q)
#     url = cur.fetchall()
#     website_q=f"Select website from gmb_profile_details where place_id='{place_id}'"
#     sql_query(website_q)
#     res = cur.fetchall()
#     website = res[0][0]
#     if website == '':
#         data = {
#             "url":"https://"+url[0][0]+".chrone.work",
#             "place_id":place_id,
#             "biz_name":data[0][0].replace("'","''"),
#             "old_gmb_website":"No website",
#             "gmb_live_date":"2022-12-15"
#         }
#         insert_sql("gmb_website_status",data)
#     else:
#         data = {
#             "url":"https://"+url[0][0]+".chrone.work",
#             "place_id":place_id,
#             "biz_name":data[0][0].replace("'","''"),
#             "old_gmb_website":website,
#             "gmb_live_date":"2023-01-05"
#         }
#         insert_sql("gmb_website_status",data)
#         print("else")

# print("done")




