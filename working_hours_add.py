ENDPOINT="db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="us-east-1c"
DBNAME="postgres"
PASS = "March2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

import psycopg2
import json
import requests
import googleapiclient.discovery as gapd
import google.oauth2.credentials
import pandas as pd
from datetime import datetime




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



# place_ids = ['ChIJa3nSd-RrK4cRuH1w7b2YTMM']

# for pid in place_ids:
#     query = f''' Select gmb_retool_profile_completion."regularHours" from gmb_retool_profile_completion where place_id='{pid}' '''
#     sql_query(query)
#     workingHours = []
#     res = cur.fetchall()
#     if res[0][0] != "{}" and res[0][0] != '':
#         for hours in json.loads(res[0][0]):
#             day = {
#                 'day':hours['openDay'],
#                 'openTime':hours['openTime'],
#                 'closeTime':hours['closeTime'],
#             }
#             workingHours.append(day)

#     query = f"update gmb_website_details set working_hours = '{json.dumps(workingHours)}' where place_id='{pid}'"
#     sql_query(query)
#     conn.commit()

# def update_sql(table, data, url):
#     query = 'update ' + table + ' set '
#     itr = 0
#     for key in data.keys():
#         itr += 1
#         val = data[key]
#         if type(val) == str:
#             val = val.replace("''","'").replace("'","''").replace("%%","%").replace("%","%%")
#             query += key + "='" + val + "'"
#         elif type(val) == dict:
#             dict_val = json.dumps(val).replace("''","'").replace("'","''").replace("%%","%").replace("%","%%")
#             query += key + "='" + dict_val + "'"
#         elif type(val) == list:
#             list_val = json.dumps(val).replace("''","'").replace("'","''").replace("%%","%").replace("%","%%")
#             query += key +"='" + list_val + "'"
#         elif type(val) == int:
#             query += key + "=" +  str(val)
#         elif type(val) == float:
#             query += key + "=" +  str(val)
#         elif type(val) == bool:
#             if val:
#                 query += key + "=" +  'true'
#             else:
#                 query += key + "=" +  'false'
#         elif val is None:
#             query += key + "=" +  "NULL"
#         if itr == len(data.keys()):
#             pass
#         else:
#             query += ', '

#     query += f" where url='{url}'"
#     try:
#         sql_query(query)
#         conn.commit()
#         return 'Success'
#     except Exception as e:
#         return str(e)
    
# def upsert_sql(table_name,data):
#     cols = str(tuple((k) for k,v in data[0].items())).replace("'","")
#     query = f"Insert into {table_name} {cols} values "

#     for d in data:
#         query += str(tuple(v if type(v)==bool else (str(v).replace("'","''").replace('"',"''") if v is not None else '') for k, v in d.items())) +", "
#     query = query.replace('"',"'").replace("\\'","'")
#     query = query[0:-2].replace("\\n","").replace("•","")
#     print(query)
#     sql_query(query)
#     conn.commit()
#     print(cur.statusmessage)


# f = open("services_celestial.json")
# service_details = json.load(f)

# res = upsert_sql("user_services",service_details)


# print(0)

# sql_q = "select biz_name,concat('https://',url,'.chrone.work') dev_url from gmb_website_details where index_template is not null order by index_template"
# sql_query(sql_q)
# res=cur.fetchall()
# fata = []
# for r in res:
#     home_resp = requests.get(r[1])
#     if home_resp.status_code != 200:
#         fata.append(r[0])
#     print(r[0])

# if len(fata)==0:
#     print("pel diya")
# else:
#     print(fata)    
#     print(0)




# for pid in place_ids:
#     query = f"Select * from gmb_website_details where place_id='{pid}'"
#     sql_query(query)
#     res=cur.fetchall()
#     if "Working hours not given" in res[0][6]:
#         print("Working hours not for : ",res[0][3])
#     print(0)
# print(0)


# services_q = "select place_id,services from gmb_website_details where services ilike '%.0%'"
# sql_query(services_q)
# res = cur.fetchall()

# for r in res:
#     place_id=r[0]
#     services=r[1].replace(".0","").replace(".00","").replace("'","''")
#     update_q = f"update gmb_website_details set services='{services}' where place_id='{place_id}'"
#     sql_query(update_q)
#     conn.commit()

disc_info = 'https://mybusinessbusinessinformation.googleapis.com/$discovery/rest?version=v1'
disc_acc = 'https://mybusinessaccountmanagement.googleapis.com/$discovery/rest?version=v1'
disc_verify = 'https://mybusinessverifications.googleapis.com/$discovery/rest?version=v1'
disc_perf = 'https://businessprofileperformance.googleapis.com/$discovery/rest?version=v1'
disc_mybiz = "https://developers.google.com/static/my-business/samples/mybusiness_google_rest_v4p9.json"

readMask="storeCode,regularHours,name,languageCode,title,phoneNumbers,categories,storefrontAddress,websiteUri,regularHours,specialHours,serviceArea,labels,adWordsLocationExtensions,latlng,openInfo,metadata,profile,relationshipData,moreHours"


def insert_sql(table, data):
    query = 'insert into ' + table + '('
    keys = list(data.keys())
    query += ', '.join(keys) + ') values ('
    itr = 0
    for key in keys:
        itr += 1
        val = data[key]
        if type(val) == str:
            val = val.replace("''","'").replace("'","''").replace("%%","%").replace("%","%%")
            query += "'" + val + "'"
        elif type(val) == dict:
            dict_val = json.dumps(val).replace("''","'").replace("'","''").replace("%%","%").replace("%","%%")
            query += "'" + dict_val + "'"
        elif type(val) == list:
            list_val = json.dumps(val).replace("''","'").replace("'","''").replace("%%","%").replace("%","%%")
            query += "'" + list_val + "'"
        elif type(val) == int:
            query += str(val)
        elif type(val) == float:
            query += str(val)
        elif type(val) == bool:
            if val:
                query += 'true'
            else:
                query += 'false'
        elif val is None:
            query += "null"
        if itr == len(keys):
            query += ')'
        else:
            query += ', '
    try:
        # send_slack_notification("db insert", "slack-notifs-test",{})
        sql_query(query)
        conn.commit()
        # send_slack_notification("db insert success", "slack-notifs-test",{})
        return 'Success'
    except Exception as e:
        return str(e)
    


sql_q = "select distinct place_id,biz_name,email,location from gmb_biz_data where biz_name ilike '%salon bou%' and email != 'salonboutique@gmail.com'"
sql_query(sql_q)
res = cur.fetchall()

all_posts = []

for r in res:
    oauth_q = f"select oauth from gmb_oauth where email='{r[2]}'"
    sql_query(oauth_q)
    oauth = cur.fetchall()

    credentials = google.oauth2.credentials.Credentials(**(json.loads(oauth[0][0])))
    my_biz = gapd.build('mybusiness', 'v4', credentials=credentials, discoveryServiceUrl=disc_mybiz)
    
    biz_info_client = gapd.build('mybusinessbusinessinformation', 'v1', credentials=credentials, discoveryServiceUrl=disc_info)
    biz_acc_client = gapd.build('mybusinessaccountmanagement', 'v1', credentials=credentials, discoveryServiceUrl=disc_acc)
    biz_perf_client = gapd.build('businessprofileperformance', 'v1', credentials=credentials, discoveryServiceUrl=disc_perf)
    biz_info = biz_acc_client.accounts().list().execute()
    biz_info_location = biz_info_client.accounts().locations().list(parent=biz_info['accounts'][0]['name'], readMask=readMask, pageSize=100).execute()
    lcs = biz_info_location['locations']
    location=lcs[0]
    for lc in lcs:
        if res[0][3] in lc['name']:
            location=lc


    resp = my_biz.accounts().locations().localPosts().list(parent=biz_info['accounts'][0]['name']+'/'+lc["name"], pageSize=100).execute()
    for post in resp['localPosts']:
        if(post['createTime'] > '2023-03-15T00:00:00.00000Z'):
            date_time = datetime.fromisoformat(post['createTime'])
            formatted_date = date_time.strftime('%d-%B-%Y')

            post_data={
                "post_id":post['name'],
                "biz_name":r[1],
                "post_content":post['summary'],
                "created_at":formatted_date
            }
            all_posts.append(post_data)
    print(len(all_posts))

posts_df = pd.DataFrame(all_posts)
posts_df.to_csv("all_posts.csv")


    

