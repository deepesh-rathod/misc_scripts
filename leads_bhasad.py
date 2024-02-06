import pandas as pd
import json

leads_data_df = pd.read_csv("leads_data.csv")

leads_data_json = leads_data_df.to_json(orient='records')

duplicate_data_id = []

leads_data_json = json.loads(leads_data_json)

for data1 in leads_data_json:
    for data2 in leads_data_json:
        if data1['name']==data2['name'] and data1['phone']==data2['phone'] and data1['customer_type']==data2['customer_type']:
            duplicate_data_id.append(data1['id'])

print(0)