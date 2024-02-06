ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "postgres"
REGION = "us-east-1c"
DBNAME = "postgres"
PASS = "March2021"
SECRET = "04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c"

import google.oauth2.credentials
import googleapiclient.discovery as gapd
import psycopg2
import pandas as pd
import json
import requests

def sql():
    global conn, cur
    try:
        conn = psycopg2.connect(
            host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS
        )
        cur = conn.cursor()
    except Exception as e:
        print("ERROR", e)


def sql_query(query):
    global cur
    try:
        cur.execute(query)
    except:
        sql()
        cur.execute(query)

def send_slack_notification(message, channel_name="media_extraction"):
    url = 'https://0yym4no4fi.execute-api.us-east-1.amazonaws.com/default/slack_channel_send_message_api'
    parameters = {'channel_name': channel_name, 'message': message}
    resp = requests.post(url, json=parameters)
    print(str(resp))

def get_medias(oauth,location):
    try:
        oauth_dict = oauth

        disc_info = 'https://mybusinessbusinessinformation.googleapis.com/$discovery/rest?version=v1'
        disc_acc = 'https://mybusinessaccountmanagement.googleapis.com/$discovery/rest?version=v1'
        disc_verify = 'https://mybusinessverifications.googleapis.com/$discovery/rest?version=v1'
        disc_perf = 'https://businessprofileperformance.googleapis.com/$discovery/rest?version=v1'
        disc_mybiz = "https://developers.google.com/static/my-business/samples/mybusiness_google_rest_v4p9.json"
        readMask="storeCode,regularHours,name,languageCode,title,phoneNumbers,categories,storefrontAddress,websiteUri,regularHours,specialHours,serviceArea,labels,adWordsLocationExtensions,latlng,openInfo,metadata,profile,relationshipData,moreHours"

        credentials = google.oauth2.credentials.Credentials(**oauth_dict)

        oauth2_client = gapd.build('oauth2', 'v2', credentials=credentials)
        profile_data = oauth2_client.userinfo().get().execute()

        my_biz = gapd.build('mybusiness', 'v4', credentials=credentials, discoveryServiceUrl=disc_mybiz)

        biz_info_client = gapd.build('mybusinessbusinessinformation', 'v1', credentials=credentials, discoveryServiceUrl=disc_info)
        biz_acc_client = gapd.build('mybusinessaccountmanagement', 'v1', credentials=credentials, discoveryServiceUrl=disc_acc)
        biz_perf_client = gapd.build('businessprofileperformance', 'v1', credentials=credentials, discoveryServiceUrl=disc_perf)


        biz_info = biz_acc_client.accounts().list().execute()
        biz_info_location = biz_info_client.accounts().locations().list(parent=biz_info['accounts'][0]['name'], readMask=readMask, pageSize=100).execute()

        lcs = biz_info_location['locations']

        location_index = 0
        lc = [lc for lc in lcs if location in lc['name']]

        print(lc[0]["name"] +  "||" + location)

        resp = my_biz.accounts().locations().media().list(parent=biz_info['accounts'][0]['name']+"/"+lc[0]["name"], pageSize=2500).execute()

        mediaItems = []
        for media in resp['mediaItems']:
            mediaItems.append(media)

        return mediaItems
    except Exception as e:
        send_slack_notification(f"Error : {str(e)}")
        return []


biz_details_query = """select distinct god.biz_name,gbd.email,go.oauth,gbd.location from gmb_retool_onboarding_details god left join gmb_biz_data gbd on gbd.uid=god.uid left join gmb_oauth go on gbd.email = go.email"""
sql_query(biz_details_query);
res = cur.fetchall()

for r in res:
    try:
        if r[2] == None or r[1] == None or r[3]==None:
            continue
        biz_name = r[0]
        email = r[1]
        oauth = json.loads(r[2])
        location = r[3]

        media_list = get_medias(oauth,location)
        media_df = pd.DataFrame(media_list)
        media_df.to_csv(f"medias/{location}.csv",index=False)
        print(0)
        send_slack_notification(f"File saved for : {biz_name}\n File : {location}.csv")
    except Exception as e:
        send_slack_notification(f"Error for : {biz_name}")

print(0)
send_slack_notification(f"<!channel> Done for all")




