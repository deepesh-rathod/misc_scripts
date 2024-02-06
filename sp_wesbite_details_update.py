ENDPOINT="database-2.cvwhw7xmj43j.ap-south-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="ap-south-1b"
DBNAME="postgres"
PASS = "January2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

disc_acc = 'https://mybusinessaccountmanagement.googleapis.com/$discovery/rest?version=v1'
disc_mybiz = "https://developers.google.com/static/my-business/samples/mybusiness_google_rest_v4p9.json"

import json
import psycopg2
import pandas as pd
import googleapiclient.discovery as gapd
import google.oauth2.credentials

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
        return str(e), 200

def get_biz_info(credentials):
    try:
        biz_acc_client = gapd.build('mybusinessaccountmanagement', 'v1'
        , credentials=credentials, discoveryServiceUrl=disc_acc)
        biz_info = biz_acc_client.accounts().list().execute()
        return biz_info
    except Exception as e:
        return str(e), 200

def get_location_db(email):
    sql_query(f"select location from gmb_oauth where email='{email}'")
    location = cur.fetchall()[0][0]
    return location


trial_place_ids=['ChIJR4980JkLK4cR3KFaICfZczA']
for p_id in trial_place_ids:
    if True:
        place_id = p_id
        try:
            email_q = f"Select email from gmb_biz_data where place_id='{place_id}'"
            sql_query(email_q)
            res = cur.fetchall()
            email = res[0][0]

            credentials = get_gapd_creds(email)
            my_biz_client = get_mybiz_client(credentials)
            biz_info = get_biz_info(credentials)
            location = get_location_db(email)
            try:
                reviews = my_biz_client.accounts().locations().reviews().list(parent=f"{biz_info['accounts'][0]['name']}/locations/{location}", pageSize=50).execute()
            except Exception as e:
                print(e)
                print(f"Error for {email} in reviews")

            revs = []
            if 'totalReviewCount' in reviews:
                if reviews['totalReviewCount'] > 4:
                    i=0
                    while i < 6:
                        for revvs in reviews['reviews']:
                            if 'comment' in revvs.keys():
                                revi = {
                                'name': revvs['reviewer']['displayName'],
                                'review': revvs['comment']
                                }
                                revs.append(revi)
                                i+=1
            
                else:
                    for revvs in reviews['reviews']:
                            if 'comment' in revvs.keys():
                                revi = {
                                'name': revvs['reviewer']['displayName'],
                                'review': revvs['comment']
                                }
                                revs.append(revi)

                review_dict={}
                for review in revs:
                    review_dict[review['name']] = review['review']
                new_dic = {}
                k = list(review_dict.items())
                k.sort(key=lambda x:len(x[1]),reverse=True)
                new_review = []
                for i in k :
                    new_dic.update({i[0]:i[1]})
                    d = {
                        'name':i[0],
                        'review':i[1]
                    }
                    new_review.append(d)

            credentials = get_gapd_creds(email)
            location_name = get_location_db(email)
            mybiz_client = get_mybiz_client(credentials)
            biz_info = get_biz_info(credentials)
            try:
                images = mybiz_client.accounts().locations().media().list(parent=biz_info['accounts'][0]['name']+"/locations/"+location_name, pageSize=2500).execute()
            except Exception as e:
                print(e)
                print(f"Error for {email}")
            
            views = []
            for i in images['mediaItems']:
                if 'insights' in i:
                    if 'viewCount' in i['insights']:
                        views.append(int(i['insights']['viewCount']))
            
            views.sort(reverse=True)

            image_list = []
            for v in views[0:30]:
                for i in images['mediaItems']:
                    if 'insights' in i:
                        if 'viewCount' in i['insights']:
                            if i['insights']['viewCount']==str(v):
                                image_list.append(i)

            imgs=[]
            for i in image_list[0:30]:
                url = i['googleUrl']
                if i['mediaFormat']=='VIDEO':
                    url = i['googleUrl'].replace('=s0','=dv')
                data={
                    'type':i['mediaFormat'],
                    'url':url,
                }
                imgs.append(data)

            db_query = f"Select * from gmb_profile_details where place_id='{place_id}'"
            sql_query(db_query)
            res = cur.fetchall()

            url = res[0][1].lower().replace(" ","-")

            if "'" in url:
                url = url.replace("'","")

            biz_name = res[0][1]
            if "'" in biz_name:
                biz_name = res[0][1].replace("'","\'\'")

            reviewss = json.dumps(new_review[0:6])

            biz_desc = res[0][6]
            if "'" in biz_desc:
                biz_desc = res[0][6].replace("'","\'\'")


            if "'" in reviewss:
                reviewss = reviewss.replace("'","")

            address = f"{res[0][11]}"

            workingHours = []
            if res[0][10] != "{}" and res[0][10] != '':
                for hours in json.loads(res[0][10]):
                    day = {
                        'day':hours['openDay'],
                        'openTime':hours['openTime'],
                        'closeTime':hours['closeTime'],
                    }
                    workingHours.append(day)
            else:
                workingHours = "Working hours not given"

            # if res[0][18] == "":
            #     insta_link = "not updated by user"
            # else:
            #     insta_link = res[0][18]            

            if res[0][4] is not None and res[0][4] != '':
                appointment_link = res[0][4]
            else:
                appointment_link = 'not updated by user'

            sp_data = {
                'url':url,
                'number':res[0][2],
                'place_id':place_id,
                'category':res[0][20],
                'biz_name':biz_name,
                'address':address,
                'insta_link':"",
                'working_hours':json.dumps(workingHours),
                'image_header':'img_head',
                'biz_desc':biz_desc,
                'services':res[0][4] or 'no appointmen link',
                'images':json.dumps(imgs),
                'testimonials':reviewss,
                'title':'Website title',
            }

            status = insert_sql('gmb_website_details',sp_data)
            print(status)

            print(f"done for {email}")
        except Exception as e:
            print("Error : ",e)
            print(f"could not do for {email}")
print(1)
