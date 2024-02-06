ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "postgres"
REGION = "us-east-1c"
DBNAME = "postgres"
PASS = "March2021"
SECRET = "04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c"

import pandas as pd
import psycopg2

def sql():
    global conn, cur
    try:
        conn = psycopg2.connect(
            host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS
        )
        cur = conn.cursor()
    except Exception as e:
        print("ERROR", e)

def sql_query(query):
    global cur
    try:
        cur.execute(query)
        conn.commit()
    except:
        sql()
        cur.execute(query)
        conn.commit()

sql()

def get_all_schemas():
    sql_query("SELECT schema_name FROM information_schema.schemata;")
    res = cur.fetchall()
    schema_names = [r[0] for r in res]
    return schema_names

def get_all_tables(schema_name):
    sql_query(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}';")
    res = cur.fetchall()
    table_names = [r[0] for r in res]
    return table_names

def get_all_columns(schema_name,table_name):
    sql_query(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{schema_name}' AND table_name = '{table_name}';")
    res = cur.fetchall()
    column_names = [r[0] for r in res]
    return column_names

def check_place_id(columns):
    return 'place_id' in columns

def check_uid(columns):
    return 'uid' in columns

def get_columns_for_all_tables():

    all_tables_info = []

    schemas = get_all_schemas()
    # schemas = ['website']

    for schema in schemas:
        tables = get_all_tables(schema)

        for table in tables:
            columns = get_all_columns(schema,table)
            
            table_info={}
            table_info['schema'] = schema
            table_info['table'] = table
            table_info['columns'] = columns
            table_info['place_id'] = check_place_id(columns)
            table_info['uid'] = check_uid(columns)

            all_tables_info.append(table_info)

    return all_tables_info

tables_info = get_columns_for_all_tables()

tables_info_df = pd.DataFrame(tables_info)
tables_info_df.to_csv("all_table_columns.csv",index=False)
print("Done!")


