ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "postgres"
REGION = "us-east-1c"
DBNAME = "postgres"
PASS = "March2021"
SECRET = "04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c"

HOST="db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT="5432"
USER="postgres"
REGION="us-east-1c"
DB_NAME="postgres"
PASS = "March2021"

from sqlalchemy.types import TIMESTAMP, DATETIME 


import psycopg2
import pandas as pd
from datetime import datetime, date, timedelta
import json
import re
from sqlalchemy import create_engine

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


bookings_df = pd.read_csv("/Users/office/Documents/line_items_dump_sorted.csv", encoding='utf-8')
# bookings_df = bookings_df.drop(bookings_df.filter(regex="^Unnamed").columns, axis=1)
# bookings_df['start_time'] = pd.to_datetime(bookings_df['start_time'], format='%d/%m/%Y %H:%M')


def init_rds():
    cluster_endpoint = f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}"
    engine = create_engine(cluster_endpoint)
    return engine
conn = init_rds()


print(0)


bookings_df.to_sql('line_items', conn, method="multi", if_exists="append", index=False, schema="scheduling")
print(0)