import os
import json
import google.oauth2.credentials
import google_auth_oauthlib
import googleapiclient.discovery as gapd
from datetime import time,timedelta
import uuid
from requests import request
import re

ENDPOINT="db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="us-east-1c"
DBNAME="postgres"
PASS = "March2021"
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
        elif type(val) == list:
            query += "'" + json.dumps(val) + "'"
        elif type(val) == int:
            query += str(val)
        elif type(val) == float:
            query += str(val)
        elif type(val) == bool:
            query += str(val)
        elif val is None:
            query += "null"
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
    
# def upsert_sql(table_name,data):
#     cols = str(tuple((k) for k,v in data[0].items())).replace("'","")
#     query = f"Insert into {table_name} {cols} values "

#     for d in data:
#         query += str(tuple(v if type(v)==bool else (v.replace("'","''").replace('"',"''") if v is not None else '') for k, v in d.items())) +", "
#     query = query.replace('"',"'").replace("\\'","'")
#     query = query[0:-2].replace("\\n","").replace("•","")
#     print(query)
#     sql_query(query)
#     conn.commit()
#     print(cur.statusmessage)

# old_website_data = []
# new_website_data = []

# query = "select id,logo_link, services_banner, services, section_data,place_id,uid from gmb_website_details where base_template ilike '%master%'"
# sql_query(query)
# res=cur.fetchall()

# for r in res:
#     data={
#         'id':r[0],
#         'logo_link':r[1],
#         'services_banner':r[2],
#         'services':r[3],
#         'section_data':r[4],
#         'place_id':r[5],
#         'uid':r[6]
#     }
#     old_website_data.append(data)

# for data in old_website_data:
#     if data['place_id']=='ChIJ_5Gm23N1K4cRv092VsetmBw-mt':
#         continue
#     logo_link = data.get('logo_link')
#     if logo_link is not None and data.get('place_id') in logo_link:
#         logo_link = logo_link.replace(data.get('place_id'),data.get('uid'))
#     services_banner = data.get('services_banner')
#     if services_banner is not None and data.get('place_id') in services_banner:
#         services_banner = services_banner.replace(data.get('place_id'),data.get('uid'))
#     services = data.get('services')
#     services_dict = json.loads(services) if services is not None else []
#     for service in services_dict:
#         cat_img = service.get('cat_img')
#         if cat_img is not None and data.get('place_id') in cat_img:
#             cat_img = cat_img.replace(data.get('place_id'),data.get('uid'))
#             service['cat_img']=cat_img
    
#     section_data = data.get('section_data')
#     for item in list(section_data.keys()):
#         section_data_child = section_data.get(item)
#         if section_data_child is not None and type(section_data_child) == dict and 'content' in list(section_data_child.keys()):
#             child_content = section_data_child.get('content')
#             if 'media' in list(child_content.keys()):
#                 section_medias = child_content.get('media')
#                 if section_medias is not None:
#                     for media in section_medias:
#                         url = media.get('url')
#                         if url is not None and data.get('place_id') in url :
#                             url = url.replace(data.get('place_id'),data.get('uid'))
#                         media['url']=url
#                     child_content['media']=section_medias
#             # section_data_child[item]=section_data_child
#         section_data[item]=section_data_child
#     id = data.get('id')

#     new_data={
#         "id":id,
#         "logo_link":logo_link,
#         "services_banner":services_banner,
#         "services":services_dict,
#         "section_data":section_data,
#         "place_id":data.get("place_id"),
#         "uid":data.get("uid")
#     }
#     new_website_data.append(new_data)

# with open('pid_uid_migrated_data_new.json', 'w', encoding='utf-8') as f:
#     json.dump(new_website_data, f, ensure_ascii=False, indent=4)
# print(0)

f = open('pid_uid_migrated_data_new.json',encoding="utf8")
website_data = json.load(f)
sql()
ids=[]

for data in website_data:
    if data['id'] in ids: continue
    services_str = json.dumps(data['services']).replace("'","''")
    section_data_str = json.dumps(data['section_data']).replace("'","''")
    update_query = f"""
update
    gmb_website_details
set
    services='{services_str}',
    section_data='{section_data_str}'::jsonb,
    logo_link='{data['logo_link']}',
    services_banner='{data['services_banner']}'
where
    id='{data['id']}' and uid='{data['uid']}'
"""
    sql_query(update_query)
    conn.commit()
    ids.append(data['id'])
    print(f"done for {data['id']}")
    print(0)
    

print(0)




    


    




