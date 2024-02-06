# ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
# PORT = "5432"
# USR = "postgres"
# REGION = "us-east-1c"
# DBNAME = "postgres"
# PASS = "March2021"
# SECRET = "04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c"

# import google.oauth2.credentials
# import googleapiclient.discovery as gapd
# import psycopg2
# import pandas as pd
# import json
# import requests
# import os

# def sql():
#     global conn, cur
#     try:
#         conn = psycopg2.connect(
#             host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS
#         )
#         cur = conn.cursor()
#     except Exception as e:
#         print("ERROR", e)


# def sql_query(query):
#     global cur
#     try:
#         cur.execute(query)
#     except:
#         sql()
#         cur.execute(query)

# def bulk_update_table(table, primary_key, data):
#     col_str = ""
#     col_list_str = ""
#     column_names = data[0].keys()

#     for i, col in enumerate(column_names):
#         if col != primary_key:
#             print(col)
#             if i==len(column_names)-1:
#                 col_str += f"{col} = c.{col}"
#             else:
#                 col_str += f"{col} = c.{col}, "
#         if i==len(column_names)-1:
#             col_list_str += f"{col}"
#         else:
#             col_list_str += f"{col}, "

#     master_values = ""
#     for j, data_json in enumerate(data):
#         value_tup = "("
#         for ind, key in enumerate(data_json.keys()):
#             if type(data_json[key])==str:
#                 data_value = f"'{data_json[key]}'"
#             else:
#                 data_value = data_json[key]
#             if ind==len(data_json.keys())-1:
#                 value_tup += str(data_value)
#             else:
#                 value_tup += f"{data_value}, "
#         value_tup += ")"

#         if j==len(data)-1:
#             master_values += value_tup
#         else:
#             master_values += f"{value_tup}, "

#     update_query = f"""update {table} as t set
#     {col_str}
# from
#     (values
#         {master_values}
#     ) as c({col_list_str})
# where
#     c.{primary_key} = t.{primary_key}"""

#     return update_query

# sql()
# path = ".//medias"

# media_csvs = os.listdir(path)

# for media in media_csvs:
#     try:
#         # if '2580413050073479716' not in media:
#         #     continue
#         media_df = pd.read_csv(path + "//" + media)
#         if 'sourceUrl' not in list(media_df.columns):
#             continue

#         location = media.replace(".csv","")
#         media_query = f"""select gbd.uid,gmt.filename,gmt.id from gmb_media_tracking gmt join gmb_biz_data gbd on gbd.uid=gmt.uid and gbd.location='{location}'"""
#         existing_medias_df = pd.read_sql(media_query,conn)
#         media_df.dropna(subset=['sourceUrl'], inplace=True)

#         file_name = media_df["sourceUrl"].str.split("/",expand=True)

#         if file_name.shape[0] == 0:
#             continue

#         media_df["filename"]=file_name[file_name.shape[1]-1]
#         merged_df = media_df.merge(existing_medias_df,how="inner",on="filename")
#         new_df = merged_df[['id','googleUrl']]
#         new_df.rename(columns = {'googleUrl':'google_url'}, inplace=True)
#         db_data = json.loads(new_df.to_json(orient="records"))

#         if len(db_data) == 0:
#             continue
#         update_query = bulk_update_table("gmb_media_tracking","id",db_data)
#         sql_query(update_query)
#         conn.commit()
#         print(existing_medias_df["uid"][0])

#         print(0)
#     except Exception as e:
#         print("Error")

# print(0)

images = [
    "jpg",
    "gif",
    "png",
    "jpeg",
    "PNG",
    "heic",
    "HEIC",
    "Heic",
    "JPG",
    "webp",
    "WEBP",
    "JPEG",
]
videos = [
    "mp4",
    "3gp",
    "ogg",
    "mpeg",
    "mov",
    "MOV",
    "MP4",
    "MPEG",
    "flv",
    "avi",
    "mkv",
]

images_tuple = tuple(images)
videos_tuple = tuple(videos)
print(0)
