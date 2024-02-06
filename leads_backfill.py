# import json
# from math import e
# import select
# from sre_constants import SUCCESS
# from sys import exception
# from tokenize import String
# from xml.etree.ElementTree import tostring
# import openai
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import pandas as pd
# from sqlalchemy import null

# import secrets_helper

# def sql():
#     global conn, cur
#     try:
#         db_creds = secrets_helper.get_secrets(prefix='DB_')
#         conn = psycopg2.connect(host=db_creds['DB_HOST'], port=db_creds['DB_PORT'], database=db_creds['DB_NAME'],
#                                 user=db_creds['DB_USER'], password=db_creds['DB_PASS'])
#         cur = conn.cursor(cursor_factory=RealDictCursor)
#         print("Loaded creds from secret manager")
#     except Exception as e:
#         print("New sql ERROR", e)

# def sql_query(query):
#     global cur
#     try:
#         cur.execute(query)
#     except:
#         sql()
#         cur.execute(query)
#     conn.commit()

# sql()
# leads_df = pd.read_sql('Select * from sp_website_form',conn)
# columns_to_check = ['last_called','last_messaged']
# leads_filtered_df = leads_df.dropna(subset=columns_to_check, how='all')
# leads_df_with_call_message_time = leads_filtered_df[['id','last_called','last_messaged']]

# # uids_with_services = leads_df_with_call_message_time['uid']
# # uids_with_services.drop_duplicates(keep=False, inplace=True)

# # service_price_df = pd.read_sql("""SELECT
# # 	services.business_id as uid,
# # 	service_variations.name,
# # 	service_variations.price
# # FROM
# # 	scheduling.services
# # 	join scheduling.service_variations on services.id=service_variations.service_id
# # WHERE
# # 	business_id::text in(SELECT uid FROM website_dev.sp_website_form_dup WHERE service is not NULL and service != 'NULL' and service != '')""",conn)



# update_data = []

# for i in range(leads_df_with_call_message_time.shape[0]):
#     row = leads_df_with_call_message_time.iloc[i]
    
#     data = {
#         'id':int(row['id']),
#         'call_text_time':[]
#     }

#     # result_df = service_price_df[(service_price_df['uid']==row['uid']) & (service_price_df['name'] == row['service'])]

#     # if(result_df.shape[0]):
#     #     price = int(result_df.iloc[0]['price']) if str(result_df.iloc[0]['price']) != 'nan' else None
#     #     data['service_price']= None if price==0 else price
#     #     update_data.append(data)

#     # print(0)

#     # if not pd.isna(row['note']) and row['note'] != "":
#     #     data['notes'].append({
#     #         "id":0,
#     #         "text":row['note'],
#     #         "deleted":False,
#     #         "created_at":None
#     #     })
#     #     update_data.append(data)

#     if not pd.isna(row['last_messaged']) and not pd.isna(row['last_called']):
#         if row['last_messaged'] > row['last_called']:
#             data['call_text_time'].append({'type':'Texted','time':row['last_messaged'].to_pydatetime().isoformat()})
#             data['call_text_time'].append({'type':'Called','time':row['last_called'].to_pydatetime().isoformat()})
#         else:
#             data['call_text_time'].append({'type':'Called','time':row['last_called'].to_pydatetime().isoformat()})
#             data['call_text_time'].append({'type':'Texted','time':row['last_messaged'].to_pydatetime().isoformat()})
#         update_data.append(data)
#         continue
    
#     if not pd.isna(row['last_messaged']):
#         data['call_text_time'].append({'type':'Texted','time':row['last_messaged'].to_pydatetime().isoformat()})
#         update_data.append(data)    
#         continue

#     if not pd.isna(row['last_called']):
#         data['call_text_time'].append({'type':'Called','time':row['last_called'].to_pydatetime().isoformat()})
#         update_data.append(data)    
#         continue



# json_string = json.dumps(update_data, indent=4, ensure_ascii=False)
# file_path = 'lead_service_price.json'  # Set your desired file path here
# with open(file_path, 'w') as file:
#     file.write(json_string)

# print(0)

import json

def bulk_update_json_table(table, primary_key, data):    
    col_str = ""
    col_list_str = ""
    column_names = data[0].keys()
    
    for i, col in enumerate(column_names):
        if col != primary_key:
            print(col)
            if i==len(column_names)-1:
                col_str += f"{col} = c.{col}"
            else:
                col_str += f"{col} = c.{col}, "
        if i==len(column_names)-1:
            col_list_str += f"{col}"
        else:
            col_list_str += f"{col}, "
    
    master_values = ""
    for j, data_json in enumerate(data):
        value_tup = "("
        for ind, key in enumerate(data_json.keys()):
            if type(data_json[key])==str:
                data_value = f"'{data_json[key]}'"
            else:
                data_value = data_json[key]
            if ind==len(data_json.keys())-1:
                value_tup += "'" + json.dumps(data_value).replace("'","''") + "'" + "::jsonb"
            else:
                value_tup += f"{data_value}, "
        value_tup += ")"

        if j==len(data)-1:
            master_values += value_tup
        else:
            master_values += f"{value_tup}, "
    
    update_query = f"""update {table} as t set 
    {col_str}
from 
    (values 
        {master_values}
    ) as c({col_list_str})
where 
    c.{primary_key} = t.{primary_key}"""
    
    return update_query

def bulk_update_table(table, primary_key, data):    
    col_str = ""
    col_list_str = ""
    column_names = data[0].keys()
    
    for i, col in enumerate(column_names):
        if col != primary_key:
            print(col)
            if i==len(column_names)-1:
                col_str += f"{col} = c.{col}"
            else:
                col_str += f"{col} = c.{col}, "
        if i==len(column_names)-1:
            col_list_str += f"{col}"
        else:
            col_list_str += f"{col}, "
    
    master_values = ""
    for j, data_json in enumerate(data):
        value_tup = "("
        for ind, key in enumerate(data_json.keys()):
            if type(data_json[key])==str:
                data_value = f"'{data_json[key]}'"
            else:
                data_value = data_json[key]
            if ind==len(data_json.keys())-1:
                value_tup += json.dumps(data_value)
            else:
                value_tup += f"{data_value}, "
        value_tup += ")"

        if j==len(data)-1:
            master_values += value_tup
        else:
            master_values += f"{value_tup}, "
    
    update_query = f"""update {table} as t set 
    {col_str}
from 
    (values 
        {master_values}
    ) as c({col_list_str})
where 
    c.{primary_key} = t.{primary_key}"""
    
    return update_query

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"File not found at {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


json_data = read_json_file('lead_service_price.json')
update_query = bulk_update_json_table('sp_website_form','id',json_data)

file_path = 'lead_service_price.txt'  # Set your desired file path here
with open(file_path, 'w') as file:
    file.write(update_query)

print(0)