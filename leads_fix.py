import json
import secrets_helper
import psycopg2
from psycopg2.extras import RealDictCursor


def sql():
    global conn, cur
    try:
        db_creds = secrets_helper.get_secrets(prefix="DB_")
        conn = psycopg2.connect(
            host=db_creds["DB_HOST"],
            port=db_creds["DB_PORT"],
            database=db_creds["DB_NAME"],
            user=db_creds["DB_USER"],
            password=db_creds["DB_PASS"],
        )
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


sql()


def bulk_update_table(table, primary_key, data):
    col_str = ""
    col_list_str = ""
    column_names = data[0].keys()

    for i, col in enumerate(column_names):
        if col != primary_key:
            print(col)
            if i == len(column_names) - 1:
                col_str += f"{col} = c.{col}"
            else:
                col_str += f"{col} = c.{col}, "
        if i == len(column_names) - 1:
            col_list_str += f"{col}"
        else:
            col_list_str += f"{col}, "

    master_values = ""
    for j, data_json in enumerate(data):
        value_tup = "("
        for ind, key in enumerate(data_json.keys()):
            if type(data_json[key]) == str:
                data_value = f"'{data_json[key]}'"
            else:
                data_value = data_json[key]
            if ind == len(data_json.keys()) - 1:
                value_tup += str(data_value)
            else:
                value_tup += f"{data_value}, "
        value_tup += ")"

        if j == len(data) - 1:
            master_values += value_tup
        else:
            master_values += f"{value_tup}, "

    update_query = f"""update {table} as t set 
    {col_str}
from 
    (values 
        {master_values}
    ) as c({col_list_str})
where 
    c.{primary_key} = t.{primary_key}"""

    return update_query


with open("leads_data.json", "r") as file:
    data = json.load(file)

filtered_data = []

for d in data:
    if d["uid"] != None:
        filtered_data.append(d)

query = bulk_update_table("sp_website_form", "id", filtered_data)

sql_query(query)


print(0)
