import os
import json
import google.oauth2.credentials
import google_auth_oauthlib
import googleapiclient.discovery as gapd

ENDPOINT="database-2.cvwhw7xmj43j.ap-south-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="ap-south-1b"
DBNAME="postgres"
PASS = "January2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

import psycopg2
import pandas as pd

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

query = "Select biz_name,booking_link from gmb_Website_details where biz_name='Xquisite Salon'"
sql_query(query)
res = cur.fetchall()
print(0)

'''to update booking links in db'''

# booking_links = pd.read_csv("booking_links.csv")

# for i in range(booking_links.shape[0]):
#     row=booking_links.iloc[i]
#     if row['appointment_link'] != '':
#         try:
#             db_q = f'''
#                 update 
#                     gmb_website_details
#                 set
#                     booking_link = '{row['appointment_link']}'
#                 where
#                     place_id='{row['place_id']}'
#             '''
#             sql_query(db_q)
#             conn.commit()
#             print('Done for : ',row['biz_name'])
#         except Exception as e:
#             print(e)
#             print('Error for : ',row['biz_name'])
#     else:
#         print('No appointment link for : ',row['biz_name'])