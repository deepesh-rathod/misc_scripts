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


# og_data = pd.read_csv("lead comms data.csv")

# new_comms_data = []

# for i in range(og_data.shape[0]):
#     row = og_data.iloc[i]
#     biz_name = row['biz_name']
#     sp_msg = row['sp_msg']
#     cust_msg = row['cust_msg']
#     booking_link = row['booking_link']

#     q_biz_name = biz_name.replace("'","''")
#     data_query = f"select url,place_id from gmb_website_details where biz_name='{q_biz_name}'"
#     sql_query(data_query)
#     res = cur.fetchall()
#     if biz_name=='BILLIONAIRE BARBERSHOP':
#         pass
#     else:
#         url=res[0][0]
#         place_id=res[0][1]


#     cust_msg_booking_link = re.search(r'(https?://\S+)', cust_msg)
#     extracted_digits = re.findall(r'\d+', cust_msg)
#     cust_msg_number = ''.join(extracted_digits)

#     formatted_cust_msg_number = '({}) {}-{}'.format(cust_msg_number[:3], cust_msg_number[3:6], cust_msg_number[6:])

#     cust_msg_new = "Hey {name}, your interest in booking with _biz_name_ has been received! To choose your preferred day and time slot,".replace("_biz_name_",biz_name)
#     if biz_name in ['ALISON ROESSLER FITNESS','Truve']:
#         cust_msg_new = "Hey {name}, your interest booking your {service} with _biz_name_ has been received! To choose your preferred day and time slot,".replace("_biz_name_",biz_name)

#     if cust_msg_booking_link:
#         if biz_name=='BILLIONAIRE BARBERSHOP':
#             cust_msg_new += "\nuse our booking link here - _link_ or alternatively call/text us on _phone_".replace("_link_",cust_msg_booking_link.group(0)).replace("_phone_",formatted_cust_msg_number)
#         else:
#             try:
#                 insert_q = f"insert into sp_booking_link (place_id,booking_link,chrone_link) values ('{place_id}','{cust_msg_booking_link.group(0)}','{url}')"
#                 sql_query(insert_q)
#                 conn.commit()
#                 new_booking_link = f"https://chroneweb.com/book/{url}"
#                 cust_msg_new += "\nuse our booking link here - _link_ or alternatively call/text us on _phone_".replace("_link_",new_booking_link).replace("_phone_",formatted_cust_msg_number)
#             except:
#                 data_q = f"select chrone_link from sp_booking_link where place_id='{place_id}'"
#                 sql_query(data_q)
#                 new_booking_link = cur.fetchall()[0][0]
#                 cust_msg_new += "\nuse our booking link here - _link_ or alternatively call/text us on _phone_".replace("_link_",new_booking_link).replace("_phone_",formatted_cust_msg_number)                
#     else:  
#        cust_msg_new += "\nPlease reach out on _phone_ as soon a possible.".replace("_phone_",formatted_cust_msg_number)

#     sp_msg_new = "Cha-Ching!\nYou just got a booking request from {cust_type} - {name} on your website!\nAct fast and call them to schedule and confirm their appointment.\nThe clock is ticking, so let's turn this booking into a success story!"

#     if biz_name in ['ALISON ROESSLER FITNESS','Truve']:
#         sp_msg_new="Cha-Ching!\nYou just got a booking request from {cust_type} on your website for _biz_name_!\nName - {name}\nService - {service}\nAct fast and call them to schedule and confirm their appointment.\nThe clock is ticking, so let's turn this booking into a success story!".replace("_biz_name_",biz_name)

#     new_comms_data.append({
#         "biz_name":biz_name,
#         "booking_link":booking_link,
#         "sp_msg_new":sp_msg_new,
#         "cust_msg_new":cust_msg_new
#     })

# new_comms_data_df = pd.DataFrame(new_comms_data)

# new_comms_data_df.to_csv("new_comms_data.csv",index=False)
    
# new_comms_data_df = pd.read_csv("new_comms_data.csv")

# for i in range(new_comms_data_df.shape[0]):
#     row = new_comms_data_df.iloc[i]
#     biz_name = row['biz_name']
#     sp_msg = row['sp_msg_new']
#     cust_msg = row['cust_msg_new']
#     booking_link = row['booking_link']

#     booking_link_q = f"select place_id,booking_link,url from gmb_website_details where biz_name='{biz_name}'"
#     sql_query(booking_link_q)
#     res=cur.fetchall()
#     if len(res):
#         place_id = res[0][0]
#         booking_link_db = res[0][1]
#         url = res[0][2]

# @tracer.wrap('method', service=constants.APP_NAME, resource='get_dead_sp_msg', span_type='web')
# def get_sp_msg(sp_msg,form_data):
#     pattern = r'{[^}]*}'
#     substrings = re.findall(pattern, sp_msg)
#     for key,value in form_data.items():
#         if key not in substrings:

#     if str(booking_link)=='nan':
#         booking_link=''

#     if booking_link_db!=booking_link:
#         try:
#             update_q = f"update sp_booking_link set booking_link={booking_link_db} where place_id={place_id}"
#             sql_query(update_q)
#             conn.commit()
#         except:
#             insert_q = f"insert into sp_booking_link (place_id,booking_link,chrone_link) values ('{place_id}','{booking_link_db}','{url}')"
#             sql_query(insert_q)
#             conn.commit()
#             new_booking_link = f"https://chroneweb.com/book/{url}"  

#             cust_msg_new = "Hey {name}, your interest in booking with _biz_name_ has been received! To choose your preferred day and time slot,".replace("_biz_name_",biz_name)
           
#             extracted_digits = re.findall(r'\d+', cust_msg)
#             cust_msg_number = ''.join(extracted_digits)
#             formatted_cust_msg_number = '({}) {}-{}'.format(cust_msg_number[:3], cust_msg_number[3:6], cust_msg_number[6:])
           
#             cust_msg_new += "\nuse our booking link here - _link_ or alternatively call/text us on _phone_".replace("_link_",new_booking_link).replace("_phone_",formatted_cust_msg_number)

#             new_comms_data_df.at[i, 'cust_msg_new'] = cust_msg_new   
#             print(f"updated for biz_name {biz_name}")             


            

# new_comms_data_df.drop_duplicates(subset="biz_name",keep=False, inplace=True)
# new_comms_data_df.to_csv("new_comms_data.csv",index=False)

# data_query = "select distinct lcd.*,god.biz_name,url from lead_comms_dynamic lcd join gmb_retool_onboarding_details god on lcd.place_id=god.place_id join gmb_website_details gwd on gwd.place_id=god.place_id order by biz_name"
# sql_query(data_query)
# res = cur.fetchall()

# new_comms_data = []

# for r in res:
#     # print(0)
    
#     place_id = r[0]
#     sp_msg = r[1]
#     cust_msg = r[2]
#     biz_name = r[6]
#     comm_type = r[3]
#     url = r[7]

#     cust_msg_booking_link = re.search(r'(https?://\S+)', cust_msg)
#     extracted_digits = re.findall(r'\d+', cust_msg)
#     cust_msg_number = ''.join(extracted_digits)
#     formatted_cust_msg_number = '({}) {}-{}'.format(cust_msg_number[:3], cust_msg_number[3:6], cust_msg_number[6:])

#     cust_msg_new = "Hey {name}, your interest in booking with _biz_name_ has been received! To choose your preferred day and time slot,".replace("_biz_name_",biz_name)
#     if biz_name in ['ALISON ROESSLER FITNESS','Truve']:
#         cust_msg_new = "Hey {name}, your interest booking your {service} with _biz_name_ has been received! To choose your preferred day and time slot,".replace("_biz_name_",biz_name)

#     booking_link = None
#     if cust_msg_booking_link:
#         booking_link=cust_msg_booking_link.group(0)
#         if biz_name=='BILLIONAIRE BARBERSHOP':
#             cust_msg_new += "\nuse our booking link here - _link_ or alternatively call/text us on _phone_".replace("_link_",cust_msg_booking_link.group(0)).replace("_phone_",formatted_cust_msg_number)
#         else:
#             try:
#                 insert_q = f"insert into sp_booking_link (place_id,booking_link,chrone_link) values ('{place_id}','{cust_msg_booking_link.group(0)}','{url}')"
#                 sql_query(insert_q)
#                 conn.commit()
#                 new_booking_link = f"https://chroneweb.com/book/{url}"
#                 cust_msg_new += "\nuse our booking link here - _link_ or alternatively call/text us on _phone_".replace("_link_",new_booking_link).replace("_phone_",formatted_cust_msg_number)
#             except:
#                 data_q = f"select chrone_link from sp_booking_link where place_id='{place_id}'"
#                 sql_query(data_q)
#                 new_booking_link = cur.fetchall()[0][0]
#                 cust_msg_new += "\nuse our booking link here - _link_ or alternatively call/text us on _phone_".replace("_link_",new_booking_link).replace("_phone_",formatted_cust_msg_number)                
#     else:  
#        cust_msg_new += "\nPlease reach out on _phone_ as soon a possible.".replace("_phone_",formatted_cust_msg_number)

#     sp_msg_new = "Cha-Ching!\nYou just got a booking request from {cust_type} - {name} on your website!\nAct fast and call them to schedule and confirm their appointment.\nThe clock is ticking, so let's turn this booking into a success story!"

#     if biz_name in ['ALISON ROESSLER FITNESS','Truve']:
#         sp_msg_new="Cha-Ching!\nYou just got a booking request from {cust_type} on your website for _biz_name_!\nName - {name}\nService - {service}\nAct fast and call them to schedule and confirm their appointment.\nThe clock is ticking, so let's turn this booking into a success story!".replace("_biz_name_",biz_name)
#     if biz_name in ['Skinsation Aesthetics']:
#         sp_msg_new="Cha-Ching!\nYou just got a booking request from {cust_type} on your website!\nName - {name}\nMessage - {message}\nAct fast and call them to schedule and confirm their appointment.\nThe clock is ticking, so let's turn this booking into a success story!".replace("_biz_name_",biz_name)
#     if biz_name in ['The Estie Babe | Beauty Salon | Day Spa | Skincare']:
#         sp_msg_new="Cha-Ching!\nYou just got a booking request from {cust_type} on your website!\nName - {name}\nEmail - {Email}\nService Requested - {Service Requested}\nAct fast and call them to schedule and confirm their appointment.\nThe clock is ticking, so let's turn this booking into a success story!".replace("_biz_name_",biz_name)
#     if biz_name in ['Solaris Dental Health','Solaris Medical Wellness']:
#         sp_msg_new="Cha-Ching!\nYou just got a booking request from {cust_type} - {name} on your website for _biz_name_!\nAct fast and call them to schedule and confirm their appointment.\nThe clock is ticking, so let's turn this booking into a success story!".replace("_biz_name_",biz_name)

#     print(f"done for {biz_name}")
#     new_comms_data.append({
#         "place_id":place_id,
#         "biz_name":biz_name,
#         "booking_link":booking_link,
#         "sp_msg_new":sp_msg_new,
#         "cust_msg_new":cust_msg_new
#     })

# new_comms_data_df.to_csv("new_comms_data.csv")

# from sqlalchemy.types import VARCHAR, DATE, INTEGER,BOOLEAN
# dtype = {
#     "place_id":VARCHAR,
#     "sp_msg":VARCHAR,
#     "cust_msg":VARCHAR,
#     "comm_type":VARCHAR,
#     "internal_update":BOOLEAN,
#     "created_at":DATE
# }

# new_comms_data_df = pd.read_csv("new_comms_data.csv")

# def init_rds():
#     cluster_endpoint = f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}"
#     engine = create_engine(cluster_endpoint)
#     return engine
# conn = init_rds()

# new_comms_data_df = new_comms_data_df.drop(['booking_link', 'biz_name'], axis=1)
# new_comms_data_df['created_at'] = str((datetime.utcnow()+timedelta(minutes=330)).date())
# new_comms_data_df['internal_update'] = True
# new_comms_data_df['sp_update'] = False
# new_comms_data_df['comm_type'] = 'phone'

# print(0)


# new_comms_data_df.to_sql('lead_comms_dynamic', conn, dtype=dtype, method="multi", if_exists="replace", index=False)

# data_query = "select distinct lcd.*,god.biz_name,url from lead_comms_dynamic lcd join gmb_retool_onboarding_details god on lcd.place_id=god.place_id join gmb_website_details gwd on gwd.place_id=god.place_id order by biz_name"
# sql_query(data_query)
# res = cur.fetchall()

# new_comms_data = []

# for r in res:
#     # print(0)
#     place_id = r[0]
#     sp_msg = r[1]
#     cust_msg = r[2]
#     biz_name = r[8]
#     comm_type = r[3]
#     url = r[9]

#     extracted_digits = re.findall(r'\d+', cust_msg)
#     cust_msg_number = ''.join(extracted_digits)

#     # print(0)
#     if len(cust_msg_number)>10:
#         print(f"flag for {biz_name} | {place_id}")

# services_df = pd.read_csv("russo.csv")
# services_list = services_df.to_json(orient="records")

# for s in json.loads(services_list):
#     s['place_id']='russomasterbarberpid'
#     insert_sql("user_services",s)
#     print(0)
