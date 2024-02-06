import pandas as pd
import json

# def dataframe_difference(df1, df2):
#     """
#     Find rows which are different between two DataFrames.
#     :param df1: first dataframe.
#     :param df2: second dataframe.
#     :return:    if there is different between both dataframes.
#     """
#     comparison_df = df1.merge(df2, indicator=True, how='outer')
#     diff_df = comparison_df[comparison_df['_merge'] != 'both']
#     return diff_df

# logs = pd.read_csv("alison_logs.csv")

# for i in range(logs.shape[0]):
#     row = logs.iloc[i]

#     try:
#         media_old = json.loads(row['old_section_data'])['gallery']['content']['media']
#         media_new = json.loads(row['new_section_data'])['gallery']['content']['media']
        
#         df_old = pd.DataFrame(media_old)
#         df_old = pd.DataFrame(media_new)
#         diff = dataframe_difference(df_old, df_old)
#         if diff.shape[0]==0:
#             print(f"no diff at {row['tstamp']}")
#             print(f"{len(media_new)}-{len(media_old)}")
#         else:
#             print(f"diff at {row['tstamp']}")
#     except Exception as e:
#         pass

# print(0)

f = open('pid_uid_migration_distinct.json',encoding="utf8")
up_data={}
website_data = json.load(f)
for data in website_data:    
    up_data[data.get('place_id')]=data.get('uid')
print(0)

with open('pid_uid_key_value_new.json', 'w', encoding='utf-8') as f:
    json.dump(up_data, f, ensure_ascii=False, indent=4)
print(0)