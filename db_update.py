import json
import pandas as pd
def upsert_sql(table_name,data):
    cols = str(tuple((k) for k,v in data[0].items())).replace("'","")
    query = f"Insert into {table_name} {cols} values "

    for d in data:
        query += str(tuple(v if type(v)==bool else (v.replace("'","''").replace('"',"''") if v is not None else '') for k, v in d.items())) +", "
    query = query.replace('"',"'").replace("\\'","'")
    query = query[0:-2].replace("\\n","").replace("•","")
    return query

website_status = pd.read_excel("website_status_old.xlsx")

website_status_json = website_status.to_json(orient="records")
bulk_inser_q = upsert_sql("gmb_website_status_new",json.loads(website_status_json))
print(0)