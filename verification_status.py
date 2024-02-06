import os
import json
import google.oauth2.credentials
import google_auth_oauthlib
import googleapiclient.discovery as gapd
import math
from datetime import datetime, timedelta
import pandas as pd


oauths_df = pd.read_csv("google_oauths.csv")

verification_data = []
oauth_failed = []

for i in range(oauths_df.shape[0]):
    row = oauths_df.iloc[i]
    oauth_dict = json.loads(row['oauth'])
    biz_name = row['biz_name']
    email = row['email']
    location = row['location']

# oauth_dict = {"token": "ya29.a0AfB_byCxaV5UcWCbkOqhrykBpvHL9OEhnaMQ1pZDGoUKRi4Pu7dtivj7aTkLssAlH-BvuWIseHuie-RSob8e-I8oeMNslPBO7xBCqgqa6fq0QLUqr0yWjgRyrq10OutIQfTbC1qZMMXYFbeugpw-YwMIUeqBaCgYKAbUSARASFQHsvYls3qq203xEgGrK2VMQKpbGzA0163", "refresh_token": "1//0doJpMZX1kMdoCgYIARAAGA0SNwF-L9IrRdsimB3BF_0kf_t3i-cm0oadipqPHNajeSGSU1XUY6gvrd55fsft7K8rW4JJV4kLNQQ", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "396419005169-0rlvknnf4suo2d8a95k91d35rn59cana.apps.googleusercontent.com", "client_secret": "RYgNazeJBJ5wh963v8QIfHL2", "scopes": ["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/business.manage", "https://www.googleapis.com/auth/businesscommunications"]}

    try:
        disc_info = 'https://mybusinessbusinessinformation.googleapis.com/$discovery/rest?version=v1'
        disc_acc = 'https://mybusinessaccountmanagement.googleapis.com/$discovery/rest?version=v1'
        disc_verify = 'https://mybusinessverifications.googleapis.com/$discovery/rest?version=v1'
        disc_perf = 'https://businessprofileperformance.googleapis.com/$discovery/rest?version=v1'
        disc_mybiz = "https://developers.google.com/static/my-business/samples/mybusiness_google_rest_v4p9.json"
        readMask="storeCode,regularHours,name,languageCode,title,phoneNumbers,categories,storefrontAddress,websiteUri,regularHours,specialHours,serviceArea,labels,adWordsLocationExtensions,latlng,openInfo,metadata,profile,relationshipData,moreHours"

        credentials = google.oauth2.credentials.Credentials(**oauth_dict)

        oauth2_client = gapd.build('oauth2', 'v2', credentials=credentials)
        profile_data = oauth2_client.userinfo().get().execute()

        print(profile_data)

        biz_info_client = gapd.build('mybusinessbusinessinformation', 'v1', credentials=credentials, discoveryServiceUrl=disc_info)
        biz_acc_client = gapd.build('mybusinessaccountmanagement', 'v1', credentials=credentials, discoveryServiceUrl=disc_acc)
        biz_verify_client = gapd.build('mybusinessverifications', 'v1', credentials=credentials, discoveryServiceUrl=disc_verify)
        biz_perf_client = gapd.build('businessprofileperformance', 'v1', credentials=credentials, discoveryServiceUrl=disc_perf)


        biz_info = biz_acc_client.accounts().list().execute()
        biz_info_location = biz_info_client.accounts().locations().list(parent=biz_info['accounts'][0]['name'], readMask=readMask, pageSize=100).execute()

        lcs = biz_info_location['locations']

        end_date = datetime.today()
        start_date = end_date - timedelta(days=10)
        def get_biz_perf_metric(client,lc_name):
            try:
                perf_metric = client.locations().getDailyMetricsTimeSeries(
                    name=lc_name,
                    dailyMetric="BUSINESS_IMPRESSIONS_DESKTOP_MAPS",
                    dailyRange_endDate_day=end_date.day,
                    dailyRange_endDate_month=end_date.month,
                    dailyRange_endDate_year=end_date.year,
                    dailyRange_startDate_day=start_date.day,
                    dailyRange_startDate_month=start_date.month,
                    dailyRange_startDate_year=start_date.year,
                ).execute()
                return True,None
            except Exception as e:
                err = json.loads(e.content)
                err_msg = err.get('error').get('message')
                return False,err_msg
            
        location = None

        for lc in lcs:
            if lc['name'].split("/")[1] == row['location']:
                location=lc 
            else:
                print("not matched")
        

        if location is not None:
            temp_data = {
                'biz_name':location['title'],
            }
            verficiation_details = biz_verify_client.locations().verifications().list(parent=lc["name"]).execute()
            if verficiation_details.get('verifications') is not None:
                verifications = []
                for verification_item in verficiation_details['verifications']:
                    v_data = {
                        'method':verification_item['method'],
                        'state': verification_item['state']
                    }
                    verifications.append(v_data)
                temp_data['verifications']=verifications
            performance_metric,err_msg = get_biz_perf_metric(biz_perf_client,location['name'])
            temp_data['performance_metric'] = performance_metric
            temp_data['performance_error'] = err_msg
            temp_data['mapsUri'] = location['metadata'].get('mapsUri')
            temp_data['newReviewUri'] = location['metadata'].get('newReviewUri')
            temp_data['location'] = location['name']

            verification_data.append(temp_data)
            print(f"done for {lc['title']}")
    except Exception as e:
        # print(0)
        oauth_failed.append({
            'biz_name':biz_name,
            'location':email
        })
        print(f"error for {biz_name}")
verification_data_df = pd.DataFrame(verification_data)
verification_data_df.to_csv("verifications.csv")

oauth_failed_df = pd.DataFrame(oauth_failed)
oauth_failed_df.to_csv("oauth_failed.csv")

