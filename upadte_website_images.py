ENDPOINT="database-2.cvwhw7xmj43j.ap-south-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="ap-south-1b"
DBNAME="postgres"
PASS = "January2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

disc_acc = 'https://mybusinessaccountmanagement.googleapis.com/$discovery/rest?version=v1'
disc_mybiz = "https://developers.google.com/static/my-business/samples/mybusiness_google_rest_v4p9.json"

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

def get_gapd_creds(email):
    sql_query("SELECT oauth FROM gmb_oauth WHERE email='"+email+"'")
    res = cur.fetchall()
    creds = json.loads(res[0][0])
    credentials = google.oauth2.credentials.Credentials(**creds)
    return credentials

def get_mybiz_client(credentials):
    try:
        my_biz_client = gapd.build('mybusiness', 'v4', credentials=credentials, discoveryServiceUrl=disc_mybiz)
        return my_biz_client
    except Exception as e:
        return str(e), 200

def get_biz_info(credentials):
    try:
        biz_acc_client = gapd.build('mybusinessaccountmanagement', 'v1'
        , credentials=credentials, discoveryServiceUrl=disc_acc)
        biz_info = biz_acc_client.accounts().list().execute()
        return biz_info
    except Exception as e:
        return str(e), 200

def get_location_db(email):
    sql_query(f"select location from gmb_oauth where email='{email}'")
    location = cur.fetchall()[0][0]
    return location

# query = "Select place_id from gmb_website_details"
# sql_query(query)
# res = cur.fetchall()

# place_ids = [r[0] for r in res]

# place_ids  = ["ChIJEbeAlgcAK4cR9UMwpcwlRR8"]

# for place_id in place_ids:
#     email_q = f"Select email from gmb_biz_data where place_id='{place_id}'"
#     sql_query(email_q)
#     res = cur.fetchall()
#     email = res[0][0]

#     credentials = get_gapd_creds(email)
#     # location_name = get_location_db(email)
#     location_name = "11157602345144242759"
#     mybiz_client = get_mybiz_client(credentials)
#     biz_info = get_biz_info(credentials)
#     try:
#         images = mybiz_client.accounts().locations().media().list(parent=biz_info['accounts'][0]['name']+"/locations/"+location_name, pageSize=2500).execute()
#     except Exception as e:
#         images = {
#             'mediaItems':[]
#         }
#         print(e)
#         print(f"Error for {email}")

#     if images == {}:
#         images = {
#             'mediaItems':[]
#         }
        
#     views = []
#     try:
#         for i in images['mediaItems']:
#             if 'insights' in i:
#                 if 'viewCount' in i['insights']:
#                     views.append(int(i['insights']['viewCount']))

#         views.sort(reverse=True)

#         image_list = []
#         for v in views[0:30]:
#             for i in images['mediaItems']:
#                 if 'insights' in i:
#                     if 'viewCount' in i['insights']:
#                         if i['insights']['viewCount']==str(v):
#                             image_list.append(i)

#         imgs=[]
#         for i in image_list[0:30]:
#             url = i['googleUrl']
#             if i['mediaFormat']=='VIDEO':
#                 url = i['googleUrl'].replace('=s0','=dv')
#             data={
#                 'type':i['mediaFormat'],
#                 'url':url,
#             }
#             imgs.append(data)

#         imgs = json.dumps(imgs)
#         update_q = f"update gmb_website_details set images='{imgs}' where place_id='{place_id}'"
#         sql_query(update_q)
#         conn.commit()
#         print(f"Updated for {email}")
#     except Exception as e:
#         print(e)
#         print(f"Error for {email}")




