from math import e
from sre_constants import SUCCESS
import psycopg2
from psycopg2.extras import RealDictCursor
from uuid import uuid4

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

def get_clients_data(uid):
    query = f"""
    SELECT
        *
    FROM
        campaigns.clients
    WHERE
        uid = '{uid}'
"""
    sql_query(query)
    res = cur.fetchall()
    return [dict(r) for r in res]

# uid = 'fb195d70-a296-4240-9bc1-4baaa90ca62a'
clients_data = get_clients_data(uid)

for i,c in enumerate(clients_data):
    user_id = str(uuid4())
    update_query = f"""
        UPDATE
            campaigns.clients
        SET
            user_id = '{user_id}'
        WHERE
            clients.id = '{c.get('id')}'
    """
    sql_query(update_query)
    conn.commit()
    print(f"Done for {i}")