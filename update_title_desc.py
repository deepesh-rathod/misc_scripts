ENDPOINT="database-2.cvwhw7xmj43j.ap-south-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="ap-south-1b"
DBNAME="postgres"
PASS = "January2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

import pandas as pd
import psycopg2

def sql():
    global conn, cur
    try:
        conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS)
        cur = conn.cursor()
    except Exception as e:
        print("ERROR",e)


def sql_query(query):
    global cur
    try:
        cur.execute(query)
    except:
        sql()
        cur.execute(query) 

sheet_id = "1mYZDaK1SVjNukN83vsnvu8P913OD1djWRl-2OsJ8xak"
sheet_name = "title_desc"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

title_desc_df = pd.read_csv(url)
place_id='ChIJCQ1aL_SpK4cRqZH6WEhnyzE'
query = f"Select place_id,biz_name,category from gmb_profile_details where place_id='{place_id}'"
sql_query(query)
res = cur.fetchall()

place_id = res[0][0]
biz_name = res[0][1]
category = res[0][2]

row = title_desc_df.loc[(title_desc_df['category']==category) & (title_desc_df['Type']=='Team')]
try:
    title = row['title'].values[0]
    desc = row['description'].values[0]
except:
    row = title_desc_df.loc[(title_desc_df['category']=='Default') & (title_desc_df['Type']=='Both')]
    title = row['title'].values[0]
    desc = row['description'].values[0]

hero_title = row['title'].values[0]
hero_desc = row['description'].values[0].replace("{biz_name}",biz_name)
hero_desc = hero_desc.replace("\'","\'\'")

print("done for : ",biz_name)

print(0)

print(0)