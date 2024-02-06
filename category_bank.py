# import pandas as pd
# import chat_gpt
# import json

# category_bank_df_raw = pd.read_csv("categories_bank.csv")

# category_bank = json.loads(category_bank_df_raw.to_json(orient="records"))

# categories_with_descriptions =[]

# for index, cat in enumerate(category_bank):
#     prompt = f"""I am a beauty service provider and primarily I deal in {cat.get('business_category')}. I am adding new services which lie under the category of {cat.get('service_category')}. I want you to suggest me few catchy and small descriptions for the same. Make sure the description is not more than 120 words. Also note that I am a SMB based in US. Now I want you to return in the descriptions in the form of json which will be like {{'description':'->primary description that fits best','descriptions':['->list of atleast 5 descriptions.']}}. Also make sure the json returned by you is in correct format and easily parsable by any json parser. Double check and make sure you provide correct json which can be easily parsed in python. Make sure to use double quotes."""
#     messages = [
#         {"role": "user", "content": prompt}
#     ]
#     gpt_result = chat_gpt.get_gpt_response(messages,None)
#     try:
#         formatted_descriptions = json.loads(gpt_result.get("choices")[0]['message']['content'])
#     except ValueError:
#         gpt_result = chat_gpt.get_gpt_response(messages,None)
#         formatted_descriptions = json.loads(gpt_result.get("choices")[0]['message']['content'])
#     except Exception as e:
#         print(f"ERROR for cat : {cat.get('business_category')}")
#         continue

#     cat = {**cat, **formatted_descriptions}
#     categories_with_descriptions.append(cat)
#     print(f"Done for cat : {cat.get('business_category')} | {cat.get('service_category')} : {index}")

#     if index%30==0:
#         file_path = f'category_bank-{index}.json'

#         # Writing the dictionary to a JSON file
#         with open(file_path, 'w') as json_file:
#             json.dump(categories_with_descriptions, json_file, indent=4)
#         categories_with_descriptions_df = pd.DataFrame(categories_with_descriptions)
#         categories_with_descriptions_df.to_csv(f"category_bank_with_descriptions-{index}.csv")
#         print(f"Saved data for : {index}")

# # File path where the JSON data will be stored
# file_path = 'category_bank.json'

# # Writing the dictionary to a JSON file
# with open(file_path, 'w') as json_file:
#     json.dump(categories_with_descriptions, json_file, indent=4)

# categories_with_descriptions_df = pd.DataFrame(categories_with_descriptions)
# categories_with_descriptions_df.to_csv("category_bank_with_descriptions.csv")


import psycopg2
from psycopg2.extras import RealDictCursor
import json

import secrets_helper

def sql():
    global conn, cur
    try:
        db_creds = secrets_helper.get_secrets(prefix='DB_')
        conn = psycopg2.connect(host=db_creds['DB_HOST'], port=db_creds['DB_PORT'], database=db_creds['DB_NAME'],
                                user=db_creds['DB_USER'], password=db_creds['DB_PASS'])
        cur = conn.cursor(cursor_factory=RealDictCursor)
        print("Loaded creds from secret manager")
    except Exception as e:
        print("New sql ERROR", e)

def sql_query(query):
    global cur
    try:
        cur.execute(query)
    except:
        sql()
        cur.execute(query)
    conn.commit()

file_path = 'category_bank.json'

# Reading data from the JSON file
with open(file_path, 'r') as json_file:
    data = json.load(json_file)

for d in data:
    query = f"""
INSERT INTO "website"."categories_bank" ("name", "images_path", "description", "business_category", "descriptions")
VALUES
        ('{str(d['service_category']).replace("'","''")}',
        '{str(d['Data Bank Folder Name']).replace("'","''")}',
        '{str(d['description']).replace("'","''")}',
        '{str(d['business_category']).replace("'","''")}',
        '{json.dumps(d['descriptions']).replace("'","''")}');
"""
    sql_query(query)
    conn.commit()
    print(f"Done for : {d['service_category']}")