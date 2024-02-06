import pandas as pd
import json

raw_df = pd.read_csv('/Users/office/Documents/booking_link_raw_new.csv')

datas = []

for i in range(raw_df.shape[0]):
    row=raw_df.iloc[i]
    uid=row['uid']
    booking_platforms = row['booking_platforms']

    booking_platform=json.loads(booking_platforms)
    if len(booking_platform)==0:
        datas.append({
            "uid":uid,
            "booking_platform":""
        })
        continue
    link = booking_platform[0].get('link',"")
    datas.append({
        "uid":uid,
        "booking_platform":link
    })

print(0)

