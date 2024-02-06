import os
import json
import google.oauth2.credentials
import google_auth_oauthlib
import googleapiclient.discovery as gapd
import math
from datetime import datetime, timedelta


oauth_dict = {"token": "ya29.a0AbVbY6MKSv32APXL1mpY8b_VpMbcHZPzxwtfj4aRQsGF7RpBzuUmMYSTubMrAXSuIvUsfg_shD0tCidxxD8sJ9vvs7vmW1VSVgY91GFLmWTOE-0RHlDWjyEXs9OnuwcRNR1k5c4g0ixXl1m4PLJ2z5N25-95tuR4aCgYKAcQSARMSFQFWKvPl0kk1nP9sEUHELUUakwjVpQ0167", "refresh_token": "1//0dZdpfpV-eS8bCgYIARAAGA0SNwF-L9IrGQpmcOmIV1fQu8I90z-CCBfTiGpnaootn_kkQSI4Bh4N0RKxDqzb1AiL1cVB00MBbuA", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "396419005169-0rlvknnf4suo2d8a95k91d35rn59cana.apps.googleusercontent.com", "client_secret": "RYgNazeJBJ5wh963v8QIfHL2", "scopes": ["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/business.manage", "https://www.googleapis.com/auth/businesscommunications"]}


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

my_biz = gapd.build('mybusiness', 'v4', credentials=credentials, discoveryServiceUrl=disc_mybiz)

biz_info_client = gapd.build('mybusinessbusinessinformation', 'v1', credentials=credentials, discoveryServiceUrl=disc_info)
biz_acc_client = gapd.build('mybusinessaccountmanagement', 'v1', credentials=credentials, discoveryServiceUrl=disc_acc)
biz_verify_client = gapd.build('mybusinessverifications', 'v1', credentials=credentials, discoveryServiceUrl=disc_verify)
biz_perf_client = gapd.build('businessprofileperformance', 'v1', credentials=credentials, discoveryServiceUrl=disc_perf)

# biz_perf_dmap = get_performance_metric(biz_perf_client, location, "BUSINESS_IMPRESSIONS_DESKTOP_MAPS", 30, 0)

end_date = datetime.today()
start_date = end_date - timedelta(days=10)

verficiation_details = biz_verify_client.locations().verifications().list(parent=lc["name"]).execute()
print(0)

try:
    perf_metric = biz_perf_client.locations().getDailyMetricsTimeSeries(
        name=f"",
        dailyMetric="BUSINESS_IMPRESSIONS_DESKTOP_MAPS",
        dailyRange_endDate_day=end_date.day,
        dailyRange_endDate_month=end_date.month,
        dailyRange_endDate_year=end_date.year,
        dailyRange_startDate_day=start_date.day,
        dailyRange_startDate_month=start_date.month,
        dailyRange_startDate_year=start_date.year,
    ).execute()
except Exception as e:
    err = json.loads(e.content)
    err_msg = err.get('error').get('message')
    print(err_msg)
print(perf_metric)