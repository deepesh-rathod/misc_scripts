ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "postgres"
REGION = "us-east-1c"
DBNAME = "postgres"
PASS = "March2021"
SECRET = "04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c"

import pandas as pd
import psycopg2
import json
import datetime

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
    
# def epoch_to_utc_datetime(epoch_timestamp):
#     utc_datetime = datetime.datetime.utcfromtimestamp(epoch_timestamp)
#     utc_datetime_str = utc_datetime.strftime('%Y-%m-%d %H:%M:%S')
#     return utc_datetime_str
    
# miss_leads_df = pd.read_csv('Missed leads - Data set.csv')

# # miss_leads_df.drop_duplicates(subset=['phone'],inplace=True)

# unique_uids = []

# for i in range(miss_leads_df.shape[0]):
#     row = miss_leads_df.iloc[i]
#     if row['Lead G.'].lower()=='no':
#         continue
#     place_id = row['place_id']
#     created_at = epoch_to_utc_datetime(row['Time'])
#     name = row['name']
#     phone = row['phone']
#     customer_type = row['customer_type']
#     biz_name = row['biz_name']

#     # if row['UTM Source'] == 'googlemaps':
#     #     continue

#     if str(place_id) == 'nan' and str(biz_name)=='nan':
#         print("ERROR for  : ",place_id)
#         continue
#     elif str(place_id) != 'nan' and 'placeid' not in place_id:
#         biz_data_query = f"Select biz_name,uid,place_id from gmb_retool_onboarding_details where place_id='{place_id}'"
#     else:
#         query_biz_name = biz_name.replace("'","''")
#         if 'Christian Nicole' in biz_name:
#             query_biz_name = 'Christian Nicoles House of Beauty'
#         if 'Queen Glam Studios' in biz_name:
#             query_biz_name = 'Glam queen studios'
#         biz_data_query = f"Select biz_name,uid,place_id from gmb_retool_onboarding_details where biz_name ilike '%{query_biz_name}%'"

#     sql_query(biz_data_query)
#     res = cur.fetchall()

#     biz_name = res[0][0]
#     uid = res[0][1]
#     place_id = res[0][2]

#     form_data = {"name":name,"phone":str(phone)}

#     print(biz_name, "|", uid, "|", place_id, "||", i)

#     utm_source = row['UTM Source']
#     initial_referrer = row['Initial Referrer']

#     if uid not in unique_uids:
#         unique_uids.append(uid)

#     if "'" in biz_name:
#         print(phone)

#     if str(utm_source) == 'nan':
#         utm_source = None 
    
#     data={
#         "created_at":created_at,
#         "biz_name":biz_name.replace("'","''"),
#         "place_id":place_id,
#         "form_data":form_data,
#         "customer_type":customer_type,
#         "initial_referrer":None,
#         "utm_source":utm_source,
#         "service":initial_referrer,
#         "uid":uid
#     }

#     form_data_str = str(form_data).replace("'","''")
#     qc_q_form_data = f"Select * from sp_website_form where form_data::text ilike '%{str(name)}%' and form_data::text ilike '%{str(phone)}%'"
#     sql_query(qc_q_form_data)
#     res = cur.fetchall()

#     if len(res) != 0:
#         continue

#     # qc_q = f"Select * from sp_website_form where created_at = '%{created_at}%'"
#     # sql_query(qc_q)
#     # # res = cur.fetchall()
#     # if len(res)==0:
#     insert_sql("sp_website_form",data)
#     print("inserted new data : ",i)
#     # print("ERROR For")
#     print(0)

#     # insert_sql("sp_website_form",data)

#     # print(0)

# print(unique_uids)
# Replace with your own database connection details

# def get_all_table_names(schema_name):
#     sql()
#     cursor = conn.cursor()

#     # Query to get all table names in the schema
#     query = """
#         SELECT table_name
#         FROM information_schema.tables
#         WHERE table_schema = %s AND table_type = 'BASE TABLE';
#     """

#     cursor.execute(query, (schema_name,))
#     table_names = [row[0] for row in cursor.fetchall()]

#     conn.close()
#     return table_names

# def get_table_columns_and_foreign_keys(schema_name, table_name):
#     sql()
#     cursor = conn.cursor()

#     # Query to get columns and foreign keys for a specific table
#     query = f"""
#         SELECT c.column_name, c.data_type,
#                kcu.constraint_name, kcu.table_name AS foreign_table_name,
#                kcu.column_name AS foreign_column_name
#         FROM information_schema.columns AS c
#         LEFT JOIN information_schema.key_column_usage AS kcu
#           ON c.table_schema = kcu.table_schema AND c.table_name = kcu.table_name AND c.column_name = kcu.column_name
#         WHERE c.table_schema = %s AND c.table_name = %s
#         ORDER BY c.ordinal_position;
#     """

#     cursor.execute(query, (schema_name, table_name))
#     columns_and_foreign_keys = []

#     for row in cursor.fetchall():
#         column_name = row[0]
#         data_type = row[1]
#         constraint_name = row[2]
#         foreign_table_name = row[3]
#         foreign_column_name = row[4]

#         if constraint_name:  # Column is part of a foreign key
#             columns_and_foreign_keys.append({
#                 'column_name': column_name,
#                 'data_type': data_type,
#                 'foreign_key': {
#                     'constraint_name': constraint_name,
#                     'foreign_table_name': foreign_table_name,
#                     'foreign_column_name': foreign_column_name
#                 }
#             })
#         else:  # Column is not part of a foreign key
#             columns_and_foreign_keys.append({
#                 'column_name': column_name,
#                 'data_type': data_type,
#                 'foreign_key': None
#             })

#     conn.close()
#     return columns_and_foreign_keys


# schema_name = 'scheduling'
# table_names = get_all_table_names(schema_name)
# table_structure = """"""
# print("--" * 40)
# for table_name in table_names:
#     print(f"Table: {table_name}")
#     table_structure += f"Table: {table_name}\n"
#     columns_and_foreign_keys = get_table_columns_and_foreign_keys(schema_name, table_name)
#     for column_info in columns_and_foreign_keys:
#         print(f"- {column_info['column_name']} ({column_info['data_type']})")
#         table_structure += f"- {column_info['column_name']} ({column_info['data_type']})\n"

#         if column_info['foreign_key']:
#             fk_info = column_info['foreign_key']
#             print(f"  Foreign Key: {fk_info['constraint_name']} references {fk_info['foreign_table_name']}({fk_info['foreign_column_name']})")
#             table_structure += f"  Foreign Key: {fk_info['constraint_name']} references {fk_info['foreign_table_name']}({fk_info['foreign_column_name']})\n"
#     print("==" * 40)
# print(20)

# business_names = [
#     'Fitness Massage Therapy LLC',
#     'Salon Renee',
#     'Pretty Kitty Club',
#     'Perfect Tan',
#     'Hair Inc',
#     'Makeup and hair by Elinor',
#     'The Art of Slay',
#     'Logan Skincare',
#     "I'D Waxx That",
#     'New You Body contouring center',
#     'Oops Upside Yo Head',
#     'Hair by Iri'
# ]

# datas = []
# i=0
# for name in business_names:
#     sql()
#     cursor = conn.cursor()
#     name = name.replace("'","''")
#     biz_name_q = f"Select * from gmb_retool_onboarding_details where biz_name ilike '%{name}%'"
#     sql_query(biz_name_q)
#     res = cur.fetchall()
#     if len(res)==0:
#         print(f"Error for : {name}")
#         continue
#     name=res[0][0]
#     uid=res[0][5]
#     data = {
#         "name":name,
#         "uid":uid
#     }
#     datas.append(data)
#     i+=1
#     print(i)

# biz_name_uid_df = pd.DataFrame(datas)
# biz_name_uid_df.to_csv("biz_name_uid_new",index=False)
# print(0)

