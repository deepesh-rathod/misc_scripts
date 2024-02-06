import os
import json
import google.oauth2.credentials
import google_auth_oauthlib
import googleapiclient.discovery as gapd
from datetime import time, timedelta
import uuid
from requests import request
import re
import boto3
import pandas

s3 = boto3.client('s3')

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


# working_hours_query = "select distinct place_id,working_hours from gmb_website_details where place_id='ChIJiwwEPsF1K4cRYXG4dc8pdN0'"
# sql_query(working_hours_query)
# res = cur.fetchall()

# for r in res:
#     place_id = r[0]
#     weekday = [
#         "MONDAY",
#         "TUESDAY",
#         "WEDNESDAY",
#         "THURSDAY",
#         "FRIDAY",
#         "SATURDAY",
#         "SUNDAY",
#     ]
#     weekday_sort = [
#         "MONDAY",
#         "TUESDAY",
#         "WEDNESDAY",
#         "THURSDAY",
#         "FRIDAY",
#         "SATURDAY",
#         "SUNDAY",
#     ]
#     working_hours = json.loads(r[1])
#     new_working_hours = []

#     try:
#         for days in working_hours:
#             if days["day"] in weekday:
#                 weekday.remove(days["day"])
#             hours = ""

#             if days["closeTime"]["hours"]==24:
#                 hours += "Open 24 hours"
#                 new_working_hours.append(data)
#                 continue

#             if days["openTime"]["hours"]==12:
#                 hours += (
#                     str(days["openTime"]["hours"])
#                     + " PM"
#                     + " - "
#                 )
#             elif days["openTime"]["hours"]>12:
#                 hours += (
#                     str(days["openTime"]["hours"] % 12)
#                     + " PM"
#                     + " - "
#                 )
#             else:
#                 hours += (
#                     str(days["openTime"]["hours"])
#                     + " AM"
#                     + " - "
#                 )

#             if days["closeTime"]["hours"]>12:
#                 hours += (
#                     str(days["closeTime"]["hours"]%12)
#                     + " PM"
#                 )
#             elif days["closeTime"]["hours"]<12:
#                 hours += (
#                     str(days["closeTime"]["hours"])
#                     + " PM"
#                 )
#             else:
#                 hours += (
#                     str(days["closeTime"]["hours"])
#                     + " PM"
#                 )

#             data = {"day": days["day"], "hours": hours}
#             new_working_hours.append(data)

#         for day in weekday:
#             data = {"day": day, "hours": "Closed"}
#             new_working_hours.append(data)

#         new_working_hours = sorted(new_working_hours, key=lambda d: weekday_sort.index(d['day']))
#         new_working_hours_str = json.dumps(new_working_hours)
#         update_q = f"update gmb_website_details set working_hours='{new_working_hours_str}' where place_id='{r[0]}'"
#         sql_query(update_q)
#         conn.commit()
#     except Exception as e:
#         print(f"Error for : {r[0]}")
#         print(str(e))
# print(0)

# data_q = "select url,place_id,section_data,id from gmb_website_details where sections::text ilike '%working_hrs/v1%'"
# sql_query(data_q)
# res = cur.fetchall()

# for r in res:
#     try:
#         url=r[0]
#         place_id=r[1]
#         section_data = r[2]

#         og_image = section_data['working_hrs']['content']['media'][0]['url']

#         src_key = og_image.replace("https://d15e7bk5l2jbs8.cloudfront.net/","").replace(".webp","_new.webp")
#         dst_key = src_key.replace("_new.webp","_1_new.webp")
#         new_url = "https://d15e7bk5l2jbs8.cloudfront.net/" + dst_key.replace("_new","")

#         og_image = section_data['working_hrs']['content']['media'].append({
#             "url":new_url,
#             "type":"PHOTO"
#         })

#         src_bucket = 'chrone-sp-website'
#         object_info = s3.head_object(Bucket=src_bucket, Key=src_key)
#         s3.copy_object(Bucket=src_bucket, CopySource={'Bucket': src_bucket, 'Key': src_key},
#                Key=dst_key, MetadataDirective='COPY', ContentType=object_info['ContentType'])

#         section_data_str = json.dumps(section_data).replace("'","''")

#         update_query = f"update gmb_website_details set section_data = '{section_data_str}' where place_id='{place_id}' and path='home'"
#         sql_query(update_query)
#         conn.commit()
#         print(f"success for {url}")
#     except Exception as e:
#         print(f"Error for {r[0]}")

update_query = """select
    tstamp,
    old_val->>'services_banner' old_services_banner,
	old_val->>'font_scheme' old_font_scheme,
    old_val->>'color_scheme' old_color_scheme,
	old_val->>'id' id
from
    logging.t_history 
where
	logging.t_history.tabname='gmb_website_details' 
order by
    tstamp desc
limit 
	213"""
sql()
update_vals_dataframe = pd.read_sql(update_query, conn)

update_vals_list = json.loads(update_vals_dataframe.to_json(orient="records"))

for update_val in update_vals_list:
    id=int(update_val['id'])
    services_banner =str(update_val['old_services_banner'])
    font_scheme = json.dumps(json.loads(update_val['old_font_scheme'])) if update_val['old_font_scheme'] is not None else 'null' 
    color_scheme = json.dumps(json.loads(update_val['old_color_scheme'])) if update_val['old_color_scheme'] is not None else 'null'

    update_data_query = "update gmb_website_details set " 
    update_data_query+= f"services_banner='{services_banner}', "
    update_data_query+= f"font_scheme='{font_scheme}', "
    update_data_query+= f"color_scheme='{color_scheme}' "
    update_data_query+= f"where id={id}"
    sql_query(update_data_query)
    conn.commit()
    print(0)

print(0)


