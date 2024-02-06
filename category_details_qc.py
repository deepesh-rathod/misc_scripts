import pandas as pd
import json
import boto3

category_details_df = pd.read_csv("category_details.csv")

def get_letters(input_string):
    return ''.join([char for char in input_string if char.isalpha()]).lower()

category_photo_bug = []




for i in range(category_details_df.shape[0]):
    row = category_details_df.iloc[i]

    name = row.get("name")
    photo_url = row.get("photo")

    if(photo_url.split("/")[-1].split(".")[0] != get_letters(name)):
        category_photo_bug.append(json.loads(row.to_json()))
    print(i)

print("done")

