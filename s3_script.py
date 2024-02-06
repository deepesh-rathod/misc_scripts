import pandas as pd
import datetime


app_data_df = pd.read_csv("app-open-with-data.csv")

place_ids = []

for i in range(app_data_df.shape[0]):

    row = app_data_df.iloc[i]
    if row["properties.place_id"] not in place_ids and str(row["properties.place_id"]) != 'nan': 
        place_ids.append(row["properties.place_id"])
    timestamp = datetime.datetime.fromtimestamp(int(row["time"])/1000)
    formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    print(formatted_timestamp)
print(0)