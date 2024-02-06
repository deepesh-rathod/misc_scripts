import psycopg2
import pandas as pd
import json
import googleapiclient.discovery as gapd
import google.oauth2.credentials
from datetime import date,datetime

ENDPOINT="db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="us-east-1c"
DBNAME="postgres"
PASS = "March2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

disc_info = 'https://mybusinessbusinessinformation.googleapis.com/$discovery/rest?version=v1'
disc_acc = 'https://mybusinessaccountmanagement.googleapis.com/$discovery/rest?version=v1'
disc_mybiz = "https://developers.google.com/static/my-business/samples/mybusiness_google_rest_v4p9.json"
# readMask="storeCode,regularHours,name,languageCode,title,phoneNumbers,categories,storefrontAddress,websiteUri,regularHours,specialHours,serviceArea,labels,adWordsLocationExtensions,latlng,openInfo,metadata,profile,relationshipData,moreHours"
readMask="name,websiteUri"

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

def insert_sql(table, data):
    query = 'insert into ' + table + '('
    keys = list(data.keys())
    query += ', '.join(keys) + ') values ('
    itr = 0
    for key in keys:
        itr += 1
        val = data[key]
        if type(val) == str:
            query += "'" + val + "'"
        elif type(val) == dict:
            query += "'" + json.dumps(val) + "'"
        elif type(val) == int:
            query += str(val)
        elif type(val) == float:
            query += str(val)
        elif val is None:
            query += "''"
        if itr == len(keys):
            query += ')'
        else:
            query += ', '
    try:
        sql_query(query)
        conn.commit()
        return 'Success'
    except Exception as e:
        print(e)
        return str(e)

def get_gapd_creds(email):
    sql_query("SELECT oauth FROM gmb_oauth WHERE email='"+email+"'")
    res = cur.fetchall()
    creds = json.loads(res[0][0])
    credentials = google.oauth2.credentials.Credentials(**creds)
    return credentials

def get_mybiz_client(credentials):
    try:
        my_biz_client = gapd.build('mybusiness', 'v4', credentials=credentials, discoveryServiceUrl=disc_mybiz)
        return my_biz_client
    except Exception as e:
        return str(e)

def get_biz_info(credentials):
    try:
        biz_acc_client = gapd.build('mybusinessaccountmanagement', 'v1'
        , credentials=credentials, discoveryServiceUrl=disc_acc)
        biz_info = biz_acc_client.accounts().list().execute()
        return biz_info
    except Exception as e:
        return str(e)

def get_location_db(email):
    sql_query(f"select location from gmb_oauth where email='{email}'")
    location = cur.fetchall()[0][0]
    return location

def get_bizinfo_location(credentials):
    biz_info_client = gapd.build('mybusinessbusinessinformation', 'v1', credentials=credentials, discoveryServiceUrl=disc_info)
    biz_info = get_biz_info(credentials)
    biz_info_location = biz_info_client.accounts().locations().list(parent=biz_info['accounts'][0]['name'], readMask=readMask).execute()
    return biz_info_location

def gmb_update_services(credentials, biz_info_location,service_list):
    biz_info_client = gapd.build('mybusinessbusinessinformation', 'v1', credentials=credentials, discoveryServiceUrl=disc_info)
    updated_service = biz_info_client.locations().patch(name=biz_info_location["locations"][0]["name"], body={"serviceItems": service_list['serviceItems']}, updateMask="serviceItems").execute()
    return updated_service

def gmb_update_openDate(credentials, biz_info_location,updateData):
    try:
        biz_info_client = gapd.build('mybusinessbusinessinformation', 'v1', credentials=credentials, discoveryServiceUrl=disc_info)
        updated_service = biz_info_client.locations().patch(name=biz_info_location["locations"][0]["name"], body=updateData, updateMask="openInfo.openingDate").execute()
        return True
    except :
        return False

def get_location_db(email):
    print(f"select location from gmb_oauth where email='{email}'")
    sql_query(f"select location from gmb_oauth where email='{email}'")
    location = cur.fetchall()[0][0]
    print("location",location)
    return location


place_ids=["ChIJOfFEDpZ7mFQRkQfA_YtTp1M"]

 
for place_id in place_ids:
    url_q = f"Select url,biz_name from gmb_website_details where place_id='{place_id}'"
    sql_query(url_q)
    data = cur.fetchall()
    biz_name=data[0][1]
    url = f"https://{data[0][0]}.chrone.work?utm_source=googlemaps&utm_medium=googlemapsprofile&utm_campaign=googlemaps"
    print(url)
    new_uri = url
    query = f"Select email from gmb_biz_data where place_id ='{place_id}'"
    sql_query(query)
    res=cur.fetchall()
    email = res[0][0]

    credentials = get_gapd_creds(email)
    biz_info = get_biz_info(credentials)
    print(biz_info)
    # my_biz_client = get_mybiz_client(credentials)
    biz_info_client = gapd.build('mybusinessbusinessinformation', 'v1', credentials=credentials, discoveryServiceUrl=disc_info)
    location = get_bizinfo_location(credentials)
    lcs = location['locations']
    lc = get_location_db(email)
    og_location = next((x for x in lcs if x['name'] == f"locations/{lc}"), None)
    website = og_location['websiteUri'] if 'websiteUri' in og_location.keys() else ''
    print(f"{biz_name} | {url} | {website}")

    try:
        resp = biz_info_client.locations().patch(name=f"locations/{lc}", body={"websiteUri": new_uri}, updateMask="websiteUri").execute()
        if website == '':
            ws_data = {
                "url":"https://"+data[0][0]+".chrone.work",
                "place_id":place_id,
                "biz_name":data[0][1].replace("'","''"),
                "old_gmb_website":"No website",
                "gmb_live_date":datetime.now().isoformat(),
                "website_type":"landing page",
                "acceptance":"no"
            }
            insert_sql("gmb_website_status",ws_data)
        else:
            ws_data = {
                "url":"https://"+data[0][0]+".chrone.work",
                "place_id":place_id,
                "biz_name":data[0][1].replace("'","''"),
                "old_gmb_website":website,
                "gmb_live_date":datetime.now().isoformat(),
                "website_type":"landing page",
                "acceptance":"no",
                "comms_send_date":""
            }
            insert_sql("gmb_website_status",ws_data)
            print("else")
        print(ws_data)
        print("done for : ",place_id)
        print("done for : ",biz_name)
    except Exception as e:
        print("error for : ",biz_name)
        # print("Error for ",place_id)
        
        print(e)

print("done for everyone!")

# ws_data = {
#     "url":"https://ink-and-wink.webflow.io/?utm_source=googlemaps&utm_medium=googlemapsprofile&utm_campaign=googlemaps",
#     "place_id":"ChIJL8apSU43K4cRAspRxlTT6zg",
#     "biz_name":"Ink & Wink Beauty",
#     "old_gmb_website":"https://ink-wink-beauty.chrone.work",
#     "gmb_live_date":"2023-01-26",
#     "website_type":"webflow"
# }
# insert_sql("gmb_website_status",ws_data)

# final_data = []
# for place_id in place_ids:
#     query = f"select gpd.biz_name,gpd.place_id,gpd.first_name,gws.url from gmb_website_status gws join gmb_profile_details gpd on gws.place_id=gpd.place_id where gws.place_id='{place_id}'"
#     sql_query(query)
#     res=cur.fetchall()
#     biz_name = res[0][0]
#     first_name = res[0][2]
#     link = res[0][3]
#     msg = f"""Hi {first_name}, we would like to share a tip with you today that could help you get more leads. If you link your Chrone website to your Instagram account, you could get more people to visit your website. Add the link to your bio section and have your Instagram followers check out your website. Your website link is - {link}
            
# Thanks,
# Team Chrone"""

#     data = {
#         "place_id":place_id,
#         "biz_name":biz_name,
#         "primary_message":msg,
#         "secondary_message":"",
#         "intent":"website_insta",
#         "type":"text"
#     }
#     final_data.append(data)

# final_data_df = pd.DataFrame(final_data)
# final_data_df.to_csv('insta_comms.csv',index=False)

