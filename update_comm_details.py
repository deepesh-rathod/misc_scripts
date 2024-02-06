
ENDPOINT="db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="us-east-1c"
DBNAME="postgres"
PASS = "March2021"

import json
import psycopg2
from datetime import datetime
import re

def old_sql():
    global conn, cur
    try:
        conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS)
        cur = conn.cursor()
        print("Loaded creds from hard coded values")
    except Exception as e:
        print("old sql ERROR", e)

old_sql()

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
    
def get_valid_phone(phone_number):
    digits = re.findall(r'\d', phone_number)[-10:]
    if len(digits):
        return ''.join(digits)
    else:
        return None
    

sql_q = """select gpc.place_id,gpc.phone,gbd.email,gpc."appointmentLink",gpc.title from gmb_retool_profile_completion gpc join gmb_biz_data gbd on gbd.place_id=gpc.place_id  where gbd.place_id in ('ChIJAxisPFwFD4gR-o9ltwuGeVo','ChIJp_55kXnwZYwRosv2ZDLQwLY','ChIJXf4GLiQHU4cRF7YV_mlbTnw')"""
sql_query(sql_q)
res=cur.fetchall()

for r in res:
    place_id=r[0]
    biz_name=r[4]
    comm_details_phn = {
        "place_id":place_id,
        "recipient":get_valid_phone(r[1]),
        "type":"phone",
        "active":"true",
        "lead_comm":"true"
    }

    comm_details_email = {
        "place_id":place_id,
        "recipient":r[2],
        "type":"email",
        "active":"true",
        "lead_comm":"false"
    }

    appointment_link=r[3]

    cust_msg = f"Hi! Your booking request with {biz_name} has been received. To make a confirmed booking immediately, you can call us at - r[1]"
    if appointment_link is not None and appointment_link != "":
        cust_msg=cust_msg+ f" or book by clicking here - {appointment_link}"

    sp_lead_msg_deails = {
        'place_id': place_id,
        "sp_msg":"Cha-Ching!\nYou have a booking request from {cust_type} - {name} on your website.\nPlease call/text them on {phone} immediately to fix an appointment.\n\nCheers,\nTeam Chrone",
        "cust_msg":cust_msg.replace("'","''"),
        "comm_type":"phone",
    }

    status_comms_phone = insert_sql('sp_comm_details',comm_details_phn)
    status_comms_email = insert_sql('sp_comm_details',comm_details_email)
    status_lead_comms = insert_sql('lead_comms_dynamic',sp_lead_msg_deails)