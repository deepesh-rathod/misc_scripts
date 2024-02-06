from math import e
from sre_constants import SUCCESS
import psycopg2
from psycopg2.extras import RealDictCursor
from uuid import uuid4
from sqlalchemy import create_engine
import pandas as pd


import secrets_helper

db_creds = secrets_helper.get_secrets(prefix="DB_")


def sql():
    global conn, cur
    try:
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


def init_rds():
    db_creds = secrets_helper.get_secrets(prefix="DB_")
    cluster_endpoint = f"postgresql://{db_creds['DB_USER']}:{db_creds['DB_PASS']}@{db_creds['DB_HOST']}:{db_creds['DB_PORT']}/{db_creds['DB_NAME']}"
    engine = create_engine(cluster_endpoint)
    return engine


engine = init_rds()

dashboard_df = pd.read_csv("uid_media_brag.csv")
dashboard_df["brag_tag"] = dashboard_df["brag_tag"].apply(
    lambda x: x.replace("4. ", "")
    .replace("1. ", "")
    .replace("2. ", "")
    .replace("3. ", "")
    .upper()
)

brag_tag_df = pd.DataFrame()

brag_tag_df = brag_tag_df.assign(
    uid=dashboard_df["uid"], rag_tag=dashboard_df["brag_tag"]
)

brag_tag_df.to_sql(
    "user_media_status",
    engine,
    schema="media",
    if_exists="append",
    method="multi",
    index=False,
)

print(0)
