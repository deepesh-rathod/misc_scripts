ENDPOINT="database-2.cvwhw7xmj43j.ap-south-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="ap-south-1b"
DBNAME="postgres"
PASS = "January2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

import json
import psycopg2
import pandas as pd
import googleapiclient.discovery as gapd
import google.oauth2.credentials

disc_info = 'https://mybusinessbusinessinformation.googleapis.com/$discovery/rest?version=v1'
disc_acc = 'https://mybusinessaccountmanagement.googleapis.com/$discovery/rest?version=v1'
disc_mybiz = "https://developers.google.com/static/my-business/samples/mybusiness_google_rest_v4p9.json"
readMask="storeCode,regularHours,name,languageCode,title,phoneNumbers,categories,storefrontAddress,websiteUri,regularHours,specialHours,serviceArea,labels,adWordsLocationExtensions,latlng,openInfo,metadata,profile,relationshipData,moreHours"

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

place_ids = ['ChIJD87alXk5NoYR5FjGlw4VHL8']

for place_id in place_ids:
    query = f"Select email from gmb_biz_data where place_id ='{place_id}'"
    sql_query(query)
    res=cur.fetchall()

    oauth_q = f"Select oauth from gmb_oauth where email='{res[0][0]}'"
    sql_query(oauth_q)
    oauth = cur.fetchall()
    oauth_dict = json.loads(oauth[0][0])

    credentials = google.oauth2.credentials.Credentials(**oauth_dict)

    oauth2_client = gapd.build('oauth2', 'v2', credentials=credentials)
    profile_data = oauth2_client.userinfo().get().execute()

    biz_info_client = gapd.build('mybusinessbusinessinformation', 'v1', credentials=credentials, discoveryServiceUrl=disc_info)
    biz_acc_client = gapd.build('mybusinessaccountmanagement', 'v1', credentials=credentials, discoveryServiceUrl=disc_acc)

    biz_info = biz_acc_client.accounts().list().execute()
    biz_info_location = biz_info_client.accounts().locations().list(parent=biz_info['accounts'][0]['name'], readMask=readMask, pageSize=100).execute()

    lcs = biz_info_location['locations']

    resp = biz_info_client.locations().get(name=lcs[1]["name"], readMask="serviceItems").execute()
    # resp = biz_info_client.locations().get(name=lcs[1]["name"], readMask="serviceItems").execute()

    services = [{
        'category':'Services',
        'services':[]
    }]

    temp_data = []

    for item in resp['serviceItems']:
        if 'freeFormServiceItem' in item.keys() and 'price' in item.keys():
            if 'description' in item['freeFormServiceItem']['label'].keys():
                if 'units' in item['price'].keys():
                    srvc = {
                        "name":item['freeFormServiceItem']['label']['displayName'],
                        "price":'$'+item['price']['units'],
                        "description":item['freeFormServiceItem']['label']['description']
                    }
                else:
                    srvc = {
                        "name":item['freeFormServiceItem']['label']['displayName'],
                        "price":'Price Varies',
                        "description":item['freeFormServiceItem']['label']['description']
                    }
                if srvc['name'] not in temp_data:
                    temp_data.append(srvc['name'])
                    services[0]['services'].append(srvc)
            else:
                if 'units' in item['price'].keys():
                    srvc = {
                        "name":item['freeFormServiceItem']['label']['displayName'],
                        "price":'$'+item['price']['units'],
                        "description":1
                    }
                else:
                    srvc = {
                        "name":item['freeFormServiceItem']['label']['displayName'],
                        "price":'Price Varies',
                        "description":1
                    }
                if srvc['name'] not in temp_data:
                    temp_data.append(srvc['name'])
                    services[0]['services'].append(srvc)
        if 'freeFormServiceItem' in item.keys():
            srvc = {
                "name":item['freeFormServiceItem']['label']['displayName'],
                "price":'Price Varies',
                "description":1
            }
            if srvc['name'] not in temp_data:
                temp_data.append(srvc['name'])
                services[0]['services'].append(srvc)

        # if 'structuredServiceItem' in item.keys():
        #     if 'description' in item['structuredServiceItem'].keys():
        #         srvc = {
        #             "name":item['structuredServiceItem']['serviceTypeId'].replace("job_type_id:","").replace("_"," ").capitalize(),
        #             "price":'Price Varies',
        #             "description":item['structuredServiceItem']['description']
        #         }
        #         if srvc['name'] not in temp_data:
        #             temp_data.append(srvc['name'])
        #             services[0]['services'].append(srvc)
        #     else:
        #         srvc = {
        #             "name":item['structuredServiceItem']['serviceTypeId'].replace("job_type_id:","").replace("_"," ").capitalize(),
        #             "price":'Price Varies',
        #             "description":1
        #         }
        #         if srvc['name'] not in temp_data:
        #             temp_data.append(srvc['name'])
        #             services[0]['services'].append(srvc)



    services = json.dumps(services)
    services = services.replace("'","\'\'")

    update_services_query = f"Update gmb_website_details set services = '{services}' where place_id='{place_id}'"
    # print(update_services_query)
    sql_query(update_services_query)
    conn.commit()

print(0)

