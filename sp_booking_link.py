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

booking_link_df = pd.read_csv("/Users/office/Documents/sp_booking_link.csv")

booking_links = []

for i in range(booking_link_df.shape[0]):
    row =  booking_link_df.iloc[i]
    uid = row['uid']
    chorne_subdomain = row['chrone_link']
    new_booking_link = f"https://{chorne_subdomain}.chrone.work/services"
    booking_links.append({
        "uid":uid,
        "booking_link":new_booking_link,
    })
    print(new_booking_link)
    
    print(0)
    
updated_query = bulk_update_table("sp_booking_link","uid",booking_links)
print(updated_query)