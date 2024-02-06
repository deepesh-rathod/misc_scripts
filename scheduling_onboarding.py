import pandas as pd
import requests
import json
import re

def remove_special_characters(input_string):
    # Define a regex pattern to match special characters (anything that is not a letter or a number)
    pattern = r'[^a-zA-Z0-9\s]'
    
    # Use re.sub to replace all matches of the pattern with an empty string
    cleaned_string = re.sub(pattern, '', input_string)
    
    return cleaned_string


scheduling_profiles_df = pd.read_csv('biz_name_uid.csv')
no_services_biz_name = []
no_data_in_db = []
no_address = []
for i in range(scheduling_profiles_df.shape[0]):
    if i>100:
        break
    row = scheduling_profiles_df.iloc[i]

    uid = row['uid']
    biz_name = row['name']

    url = f"http://chrone-dev-node-env.eba-t5g6xad2.us-east-1.elasticbeanstalk.com/schedule/onboard?id={uid}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if(response.status_code != 200):
        print(response.json())
        if response.json().get('error')=='No services found':
            no_services_biz_name.append(biz_name)
        elif response.json().get('error')=='No details found for the given business.':
            no_data_in_db.append(biz_name)
        elif response.json().get('error')=='null value in column "address" of relation "businesses" violates not-null constraint':
            no_address.append(biz_name)
        else:
            print(0)




    data = response.json()
    
    file_name = remove_special_characters(biz_name).replace(" ","_").lower()

    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"done for : {biz_name}", i)

print(0)
