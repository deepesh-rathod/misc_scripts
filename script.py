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
import psycopg2.extras
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

    query += f" where place_id='{place_id}' and path='home'"
    try:
        sql_query(query)
        conn.commit()
        return "Success"
    except Exception as e:
        return str(e)


sections_query = "select url,biz_name,sections,id from gmb_website_details where sections::text ilike '%134%'"
sql_query(sections_query)
res = cur.fetchall()

# sql_data = []

# for rr in res:
#     print(sql_data.append(dict(rr)))

for r in res:
    url = r[0]
    biz_name = r[1]
    sections = r[2]
    id = r[3]

    for section in sections:
        if str(section['id'])=='134':
            section['id']='157'
    
    sections_str = json.dumps(sections)
    update_section_query = f"update gmb_website_details set sections='{sections_str}' where id='{id}'"
    print(update_section_query)
    sql_query(update_section_query)
    conn.commit()
    print(cur.statusmessage)
    print(f"Done for : {biz_name}")


