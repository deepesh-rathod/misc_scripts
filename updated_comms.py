import pandas as pd
import json

raw_data_df = pd.read_csv('new_sp_raw_data.csv')


new_data = []
for i in range(raw_data_df.shape[0]):
    biz_name = raw_data_df.iloc[i]['biz_name']
    form_data = json.loads(raw_data_df.iloc[i]['form_data'])
    sp_msg = raw_data_df.iloc[i]['sp_msg']
    created_at = raw_data_df.iloc[i]['created_at']
    cust_type = raw_data_df.iloc[i]['customer_type']
    recipient = raw_data_df.iloc[i]['recipient']
    for key,value in form_data.items():
        sp_msg = sp_msg.replace(f"{{{key}}}",f"{value}")
    sp_msg = sp_msg.replace(f"{{cust_type}}",f"{cust_type}")
    new_data.append({
        "sp_msg":sp_msg,
        "biz_name":biz_name,
        "recipient":recipient
    })

    # print(0)

new_data_df = pd.DataFrame(new_data)
new_data_df.to_excel("comms_to_be_sent.xlsx")