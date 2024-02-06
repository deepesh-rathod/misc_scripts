import psycopg2
from psycopg2.extras import RealDictCursor
import secrets_helper
from datetime import datetime, timedelta
import boto3


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


def get_website_images():
    query = """
        SELECT
            uid,
            media_gallery
        FROM
            website."data"
    """
    sql_query(query)
    res = cur.fetchall()
    if len(res) > 0:
        return [dict(r) for r in res]
    return []


def tag_s3_object(bucket_name, object_key, tags):
    s3_client = boto3.client("s3")
    tag_set = [{"Key": key, "Value": value} for key, value in tags.items()]
    s3_client.put_object_tagging(
        Bucket=bucket_name, Key=object_key, Tagging={"TagSet": tag_set}
    )


def main():
    website_images = get_website_images()
    tags = {"backfill": "true", "destination": "website", "section": "gallery"}
    bucket_name = "chrone-sp-website"
