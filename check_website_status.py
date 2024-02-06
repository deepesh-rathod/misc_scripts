import requests
import pandas as pd
import time

urls_df = pd.read_csv('latest_urls.csv')


for i in range(urls_df.shape[0]):
    row = urls_df.iloc[i]
    url = f"https://{row['url']}.chrone.ai"
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    # time.sleep(3)
    if response.status_code != 200:
        print(f"failed | {url}")
    else:
        pass
        # print(f"success | {url}")