import os
import json
import google.oauth2.credentials
import google_auth_oauthlib
import googleapiclient.discovery as gapd
from datetime import time, timedelta
import uuid
from requests import request
import re

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


def insert_sql(table, data):
    query = "insert into " + table + "("
    keys = list(data.keys())
    query += ", ".join(keys) + ") values ("
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
            query += "NULL"
        if itr == len(keys):
            query += ")"
        else:
            query += ", "
    try:
        sql_query(query)
        conn.commit()
        return "Success"
    except Exception as e:
        print(e)
        return str(e)


def update_sql(table, data, place_id):
    query = "update " + table + " set "
    itr = 0
    for key in data.keys():
        itr += 1
        val = data[key]
        if type(val) == str:
            val = (
                val.replace("''", "'")
                .replace("'", "''")
                .replace("%%", "%")
                .replace("%", "%%")
            )
            query += key + "='" + val + "'"
        elif type(val) == dict:
            dict_val = (
                json.dumps(val)
                .replace("''", "'")
                .replace("'", "''")
                .replace("%%", "%")
                .replace("%", "%%")
            )
            query += key + "='" + dict_val + "'"
        elif type(val) == list:
            list_val = (
                json.dumps(val)
                .replace("''", "'")
                .replace("'", "''")
                .replace("%%", "%")
                .replace("%", "%%")
            )
            query += key + "='" + list_val + "'"
        elif type(val) == int:
            query += key + "=" + str(val)
        elif type(val) == float:
            query += key + "=" + str(val)
        elif type(val) == bool:
            if val:
                query += key + "=" + "true"
            else:
                query += key + "=" + "false"
        elif val is None:
            query += key + "=" + "NULL"
        if itr == len(data.keys()):
            pass
        else:
            query += ", "

    query += f" where place_id='{place_id}'"
    try:
        sql_query(query)
        conn.commit()
        return "Success"
    except Exception as e:
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

# query = "Select gwd.*,gbd.email from gmb_website_details gwd join gmb_biz_data gbd on gbd.place_id=gwd.place_id where gwd.place_id='ChIJ4TKsUdFdK4cRSD8WGQMJrMA'"
# sql_query(query)
# res=cur.fetchall()
# for r in res:
#     images = json.loads(r[12])
#     for i in images:
#         i["active"]=True
#     place_id=r[0]
#     section_data={
#         "banner":{
#             "title":r[18],
#             "description":r[19],
#             "media":[{
#                 "desktop":{
#                     "url":r[17],
#                     "type":"PHOTO"
#                 },
#                 "mobile":{
#                     "url":r[17],
#                     "type":"PHOTO"
#                 }
#             }],
#         },
#         "working_hrs":{
#             "title":"NULL",
#             "description":"null",
#             "media":[{
#                 "desktop":{
#                     "url":"null",
#                     "type":"PHOTO"
#                 },
#                 "mobile":{
#                     "url":"null",
#                     "type":"PHOTO"
#                 }
#             }]
#         },
#         "services":{
#             "title":"Services",
#             "description":"We offer a full range of high-end, top-quality services using the best beauty products and styling.",
#             "media":[{
#                 "desktop":{
#                     "url":"null",
#                     "type":"PHOTO"
#                 },
#                 "mobile":{
#                     "url":"null",
#                     "type":"PHOTO"
#                 }
#             }]
#         },
#         "gallery":{
#             "title":"Gallery",
#             "description":"Get a glimpse of our services with our inspiring gallery of images.",
#             "media":images
#         },
#         "testimonials":{
#             "title":"Testimonials",
#             "description":"Hear from our best customers, sharing their experiences with us!",
#             "media":[{
#                 "desktop":{
#                     "url":"null",
#                     "type":"PHOTO"
#                 },
#                 "mobile":{
#                     "url":"null",
#                     "type":"PHOTO"
#                 }
#             }]
#         },
#         "contact_form":{
#             "title":"Make an Appoinment",
#             "description":"Book your appointment now by filling in the following details.",
#             "media":[{
#                 "desktop":{
#                     "url":"null",
#                     "type":"PHOTO"
#                 },
#                 "mobile":{
#                     "url":"null",
#                     "type":"PHOTO"
#                 }
#             }]
#         },
#     }
#     common_data={
#             "phone":r[8],
#             "address":r[4],
#             "email":r[26],
#             "booking_link":r[14],
#             "reservation_cta":r[20],
#             "submit_cta":r[23],
#         }

#     update_data={
#         "section_data":section_data,
#         "common":common_data
#     }
#     update_sql("gmb_website_details",update_data,"ChIJOfFEDpZ7mFQRkQfA_YtTp1M")
#     print(0)
# print(0)

# i=0
# place_ids = ['ChIJ19-9z7j3XIYRGGVIE6DhbvY']
# for place_id in place_ids:
#     website_services=[]
#     services_q = f"select * from user_services where place_id='{place_id}'"
#     sql_query(services_q)
#     res=cur.fetchall()
#     service_cats = []
#     for r in res:
#         if r[2] not in service_cats:
#             service_cats.append(r[2])

#     for cat in service_cats:
#         data = {
#             "website category": cat,
#             "cat_img": f"https://chrone-website.s3.us-east-2.amazonaws.com/{place_id}/cat_{i}.webp",
#             "cat_desc": "Some random description which should be stored in category and description bank.",
#             "services": []
#         }
#         for r in res:
#             if r[2]==cat:
#                 price=''
#                 if r[8]=='STARTS_FROM':
#                     price='$'+str(res[0][9])+'+'
#                 elif r[8]=='FIXED':
#                     price='$'+str(res[0][9])
#                 elif r[8]=='RANGE':
#                     price = '$'+str(res[0][9])+'-'+'$'+str(res[0][6])
#                 elif r[8]=='NO_PRICE':
#                     price=''
#                 data['services'].append({
#                     'name':r[1],
#                     'price':price,
#                     'description':r[3]
#                 })
#         website_services.append(data)
#         i += 1
#     website_services = json.dumps(website_services)
#     website_services = website_services.replace("'", "''")

#     update_q = f"update gmb_website_details set services='{website_services}' where place_id='{place_id}'"
#     sql_query(update_q)
#     conn.commit()

# print(0)

# sql_q = "select url from gmb_website_status_new"
# sql_query(sql_q)
# res = cur.fetchall()

# for r in res:
#     url = r[0]

# print(0)


# sql_q = "select "
section_data_q = "select biz_name from gmb_website_details where index_template ilike '%new%'"
sql_query(section_data_q)
res = cur.fetchall()

for r in res:
    if r[0] in ['BossLady Hair Studio','ALISON ROESSLER FITNESS']:
        srvc = "service_template"
    elif r[0] in ["Aesthetics by Anaili"]:
        srvc = "service_template_v3"
    elif r[0] in ["Nail Love AZ"]:
        srvc="service_template_v4"
    elif r[0] in ["Modernly Smooth Wax Spa"]:
        srvc="service_template_v5"
    elif r[0] in ["Cibola’h Aesthetics & Beauty"]:
        srvc="service_template_v6"
    elif r[0] in ['The Lazy Day']:
        srvc="service_template_v7"
    elif r[0] in ['EZ Flow Drain and Sewer Services']:
        srvc="service_template_v8"
    else:
        srvc="service_template_v2"
    # cat_img = r[1]
    # section_data = r[2]
    # section_data['gallery']['media'] = images
    # update_data = json.dumps(section_data).replace("'","''")
    # update_q = f"update gmb_website_details set section_data='{update_data}' where place_id='{r[0]}'"
    # sql_query(update_q)
    # conn.commit()
    # print(f"done for {r[3]}")

    update_service_template_q = f"update gmb_website_details set service_template='{srvc}' where biz_name='{r[0]}'"
    sql_query(update_service_template_q)
    conn.commit()
    print(f"done for {r[0]}")
print(0)



print(0)
