import pandas as pd
import json

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
                value_tup += str(data_value)
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

services_with_duration_df = pd.read_csv("/Users/office/Downloads/Scheduling Biz - FINAL DURATION (16).csv", encoding="utf-8")

uids = ["4bf6bfda-b596-4b99-8ba8-a31066fe3e3d"]

for uid in uids:

    filtered_df = services_with_duration_df[services_with_duration_df['uid'] == uid]

    new_df = pd.DataFrame()
    new_df['service_id'] = filtered_df['service_id']
    new_df['duration'] = filtered_df['duration']
    # new_df['category'] = filtered_df['category']
    # new_df['pricing_type'] = filtered_df['pricing_type']
    # new_df['price_start'] = filtered_df['price_start']

    new_df_json = json.loads(new_df.to_json(orient="records"))

    bulk_update_query = bulk_update_table("user_services","service_id",new_df_json)

    bulk_update_query=bulk_update_query.replace('None','null')
    bulk_update_query=bulk_update_query.replace(".0","")
    print(bulk_update_query)



print(0)