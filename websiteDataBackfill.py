import json
from math import e
import select
from sre_constants import SUCCESS
from sys import exception
import openai
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd

import secrets_helper


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


def bulk_insert_sql(table, data, conn=None):
    if not data:
        return  # Nothing to insert

    keys = list(data[0].keys())
    columns = ", ".join(keys)

    placeholders = "(" + ", ".join(["%s"] * len(keys)) + ")"

    query = f"INSERT INTO {table} ({columns}) VALUES {placeholders}"
    query += " RETURNING *"

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)

        query_results = []

        for entry in data:
            values = []
            for key in keys:
                val = entry[key]
                if val is None:
                    values.append(None)
                elif isinstance(val, str):
                    values.append(val)
                elif isinstance(val, bool):
                    # Convert True/true to PostgreSQL boolean format
                    values.append(str(val).lower())
                elif isinstance(val, (int, float)):
                    values.append(val)
                else:
                    # Convert other types to JSON string
                    json_val = json.dumps(val)
                    values.append(json_val)

            cur.execute(query, tuple(values))
            result = cur.fetchone()
            query_results.append(result)

        cur.close()
        conn.commit()
        return query_results
    except Exception as e:
        conn.rollback()
        raise e


OPENAI_ORG_ID = "org-yM6MbuKD6qh8UR63H72ljeG1"  # get_secret_value('OPENAI_ORG_ID')
OPENAI_API_KEY = "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"  # get_secret_value('OPENAI_API_KEY')

openai.organization = OPENAI_ORG_ID
openai.api_key = OPENAI_API_KEY


def get_chat_gpt_answer(messages):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0
    )
    return completion.choices[0]["message"]["content"]  # type: ignore


def get_categories_description(services, categories):
    message = f"""following is a list of beauty services of my business: "{str(services)}". Which are categorised into following categories {str(categories)}. Give me a short service desc for each category. Make it singular and generic. Make it 1 liner, and something simple. I want to eliminate our/we/my/I. Don't include {{}} in the ouput. Eg:- "Experience the ultimate smoothness with an exceptional service. Feel confident and carefree in your own skin.  Don't correct any spellings in the final result. Use the original spellings. Return the output in the form of json. {{category name: description}}"""
    messages = [{"role": "user", "content": message}]
    try:
        print(messages)
        ans = get_chat_gpt_answer(messages)
        ans_json = json.loads(ans[: ans.index("}") + 1])
    except:
        # logger.error()
        return {}
        raise
    return ans_json


def get_letters(input_string):
    return "".join([char for char in input_string if char.isalpha()]).lower()


def insert_categories(service_categories, uid):
    formatted_categories = []
    categories = service_categories.get("service_categories", {})
    for cat in categories:
        formatted_category = {
            "name": cat.get("website category"),
            "description": cat.get("cat_desc"),
            "photo": cat.get("cat_img"),
            "business_id": uid,
        }
        formatted_categories.append(formatted_category)

    # insert categories in DB

    inserted_data = bulk_insert_sql("scheduling.categories", formatted_categories, conn)
    categories_in_db = []
    for data in inserted_data:
        categories_in_db.append(dict(data))
    return categories_in_db


def insert_services(services, categories, uid):
    categories_with_id = {}
    for cat in categories:
        categories_with_id[cat["name"]] = cat["id"]

    formatted_services = []
    for service in services:
        formatted_service = {
            "business_id": uid,
            "name": service.get("name"),
            "description": service.get("description"),
            "category": service.get("category"),
            "category_id": categories_with_id.get(service.get("category", "").strip()),
        }
        formatted_services.append(formatted_service)

    # insert services in DB

    inserted_data = bulk_insert_sql("scheduling.services", formatted_services, conn)
    services_in_db = []
    for data in inserted_data:
        services_in_db.append(dict(data))
    return services_in_db


def format_duration(duration):
    if (
        duration == ""
        or duration is None
        or duration == "null"
        or duration == "NULL"
        or duration == "Null"
    ):
        return None
    else:
        return int(float(duration))


def format_price(price):
    try:
        if (
            price == ""
            or price is None
            or price == "null"
            or price == "NULL"
            or price == "Null"
        ):
            return None
        else:
            formatted_price = float(price)
            return formatted_price
    except Exception as e:
        print(e)


def insert_service_variation(services, formatted_services):
    try:
        services_with_id = {}
        for service in formatted_services:
            services_with_id[service["name"] + service["category"]] = service["id"]

        formatted_service_variations = []
        for variants in services:
            service_variant = {
                "service_id": services_with_id[
                    variants.get("name") + variants.get("category")
                ],
                "name": variants.get("name"),
                "duration": format_duration(variants.get("duration")),
                "price": format_price(variants.get("price_start")),
                "pricing_type": variants.get("pricing_type"),
                "description": variants.get("description"),
                "price_end": variants.get("price_end"),
            }
            formatted_service_variations.append(service_variant)

        # insert services in DB
        inserted_data = bulk_insert_sql(
            "scheduling.service_variations", formatted_service_variations, conn
        )
        services_variations_in_db = []
        for data in inserted_data:
            services_variations_in_db.append(dict(data))
        return services_variations_in_db
    except Exception as e:
        print(e)


def get_new_services(services, service_categories, uid):
    try:
        formatted_categories = insert_categories(service_categories, uid)
        formatted_services = insert_services(services, formatted_categories, uid)
        formatted_service_variations = insert_service_variation(
            services, formatted_services
        )

        return formatted_categories, formatted_services, formatted_service_variations
    except Exception as e:
        print(e)


def get_profile_data(uid):
    profile_data_q = f"select * from gmb_retool_onboarding_details where uid='{uid}'"
    sql_query(profile_data_q)
    result = cur.fetchall()
    return dict(result[0]) if len(result) > 0 else {}


def get_user_services_data(services, service_variations, profile_data):
    user_services = []

    for service in services:
        service_variation = next(
            (sv for sv in service_variations if sv.get("service_id") == service["id"]),
            {},
        )
        user_service = {
            "place_id": profile_data["place_id"],
            "name": service["name"],
            "category": service["category"],
            "description": service["description"],
            "star": None,
            "service_id": service["id"],
            "price_end": service_variation.get("price"),
            "currency": None,
            "pricing_type": service_variation.get("pricing_type"),
            "price_start": service_variation.get("price"),
            "created_at": str(service["created_at"]),
            "duration": service_variation.get("duration"),
            "location_id": profile_data["location"],
            "uid": profile_data["uid"],
        }

        user_services.append(user_service)
    return user_services


def get_user_services(uid):
    user_services_q = f"select * from user_services where uid='{uid}'"
    sql_query(user_services_q)
    result = cur.fetchall()
    services = []
    for data in result:
        services.append(dict(data))
    return services


def get_service_categories(uid):
    service_category_q = (
        f"select distinct service_categories from website.data where uid='{uid}'"
    )
    sql_query(service_category_q)
    result = cur.fetchall()
    # services_categories = []
    return dict(result[0]) if len(result) > 0 else {}


def get_pro_and_schedule(uid):
    pro_schedule_q = f"""
    SELECT
        pros.id as pro_id,
        schedules.id as schedule_id
    FROM
        scheduling.pros
        join scheduling.schedules on schedules.pro_id=pros.id and pros.business_id = '{uid}'
    """
    sql_query(pro_schedule_q)
    result = cur.fetchall()
    return dict(result[0]) if len(result) > 0 else {}


def insert_pro_schedule_mapping(pro_schedule_data, services):
    data = []
    for service in services:
        data.append(
            {
                "pro_id": pro_schedule_data["pro_id"],
                "schedule_id": pro_schedule_data["schedule_id"],
                "service_id": service["id"],
            }
        )

    inserted_data = bulk_insert_sql("scheduling.pro_schedule_service", data, conn)
    pro_schedule_service_data = []
    for data in inserted_data:
        pro_schedule_service_data.append(dict(data))
    return pro_schedule_service_data


def get_services_from_csv(uid, uid_file):
    file_name = next((d["file_name"] for d in uid_file if d["uid"] == uid), "")
    services_df = pd.read_csv(file_name)
    services_list = json.loads(services_df.to_json(orient="records"))
    return services_list


def handler(uid):
    # uid_file = [{"uid":"d5b18101-0fbd-4542-92d2-e49835377923","file_name":"vanice-allure.csv"},
    # {"uid":"98af9511-a070-4987-9d61-8f2d117c0ce5","file_name":"gliss-aesthetics.csv"},
    # {"uid":"e8ec1ee2-a658-4546-93ee-4f18e1cdd191","file_name":"styles-by-torres.csv"}]
    try:
        services = get_user_services(uid)
        # services = get_services_from_csv(uid,uid_file)
        service_categories = get_service_categories(uid)

        if uid is None:
            return {
                "statusCode": 400,
                "status": "error",
                "data": {"code": "bad_request", "message": "UID not given"},
            }

        # categories = list(set([c['category'] for c in services]))
        # category_descriptions = get_categories_description(services,categories)

        categories, services, service_variations = get_new_services(
            services, service_categories, uid
        )

        # pro_schedule_data = get_pro_and_schedule(uid)
        # insert_pro_schedule_mapping(pro_schedule_data,services)

        return {"status": "SUCCESS"}
    except exception as e:
        return {"status": "ERROR", "error": e}

    # profile_data = get_profile_data(uid)

    # user_services = get_user_services_data(services,service_variations,profile_data)


def get_uids():
    #     uid_q = """
    # SELECT
    # 	uid,
    # 	biz_name
    # FROM
    # 	website. "data"
    # WHERE
    # 	uid in(
    # 		SELECT
    # 			uid FROM gmb_retool_dead_profiles
    # 		WHERE
    # 			uid in( SELECT DISTINCT
    # 					uid FROM website. "data"
    # 				WHERE
    # 					uid NOT in( SELECT DISTINCT
    # 							business_id::text FROM scheduling.categories))
    # 					AND dead IS FALSE)
    # 	AND uid NOT in('test-f8ef614e-17a6-4062-bb28-fea121905a93', 'e5e3a8ea-417d-4ea0-a51b-fa8aa8c828d0', '0051579a-902f-4274-8759-bb4652c79a92', 'e04cb16e-bbe0-40f9-9c3d-546ccebe2e8d', '7c34b3c9-ef36-4716-a75b-ed09da314936', '128ea9be-8584-4127-9164-1631e07ebd1d', 'f2124b5a-1672-42de-ad12-b8b77e16ee1e', 'f46ae1de-b97b-448c-95a8-8ecd951da588', '4ba7251a-ce6e-4348-bdd6-a10273280a7c', '4ba7251a-ce6e-4348-bdd6-a10273280a7c', 'd8ec6bd5-e5b9-40d1-be28-e6df739a87ad', 'ae2b69f1-e4e8-4c03-92aa-30611a4a8e9c', 'd07d44f3-795b-4322-a4e0-7962102f835b')
    #     """

    # uid_q = "SELECT uid,biz_name FROM gmb_retool_onboarding_details WHERE uid='d48d0b60-ec2a-4b6e-8120-87d7fa9a7a68'"

    uid_q = """SELECT uid,biz_name FROM website."data" WHERE uid='426315ef-cb45-4664-b449-98913242bd74'"""

    sql_query(uid_q)
    result = cur.fetchall()
    uids = []
    for data in result:
        uids.append(dict(data))
    return uids


backfill_results = []
uids = get_uids()
sql()
for d in uids:
    print("Started backfill for : ", d["biz_name"])
    result = handler(d["uid"])
    backfill_results.append(
        {
            "uid": d["uid"],
            "biz_name": d["biz_name"],
            "status": result.get("status"),
            "error": result.get("error"),
        }
    )
    print("Completed backfill for : ", d["biz_name"])

print(0)
