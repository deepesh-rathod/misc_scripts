import pandas as pd

df = pd.read_csv('landingpages_new.csv')
new_lst=[]
for i in range(df.shape[0]):
    row = df.iloc[i]
    dic={
    "place_id":row['place_id'],
    "biz_name":row['biz_name'],
    "category":row['category'],
    "status":"",
    "live_url":f"https://{row['url']}.chrone.work",
    "QC":"",
    }
    new_lst.append(dic)

new_df = pd.DataFrame(new_lst)
new_df.to_csv("new_live_urls.csv",index=False)
    
