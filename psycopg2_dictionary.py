import psycopg2
from psycopg2.extras import RealDictCursor

ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "postgres"
REGION = "us-east-1c"
DBNAME = "postgres"
PASS = "March2021"
SECRET = "04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c"

def fetch_data_from_db(query, params=None):
    # Database connection parameters - modify as needed
    db_params = {
        'dbname': DBNAME,
        'user': USR,
        'password': PASS,
        'host': ENDPOINT,
        'port': PORT
    }

    conn = None
    result = []

    try:
        conn = psycopg2.connect(**db_params)
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
    
    return result

# Example usage

def convert_rows_to_dicts(rows):
    return [dict(row) for row in rows]


uid = "db2a4f38-38cd-464e-b519-91a4b44230e3"
services_query = "Select * from user_services where uid = %s"
services_raw_data = fetch_data_from_db(services_query, (uid,))
services_data = convert_rows_to_dicts(services_raw_data)
print(services_data)

categories_query = "Select service_categories from website.data where uid = %s"
categories_raw_data = fetch_data_from_db(services_query, (uid,))
categories_data = convert_rows_to_dicts(categories_raw_data)
print(categories_data)

async def add_service_categories(data):
    services = data.get("services", [])
    categories = data.get("categories", [{}])[0].get("service_categories", [])

    categories_data = []
    slack_msg = "Missing Service Details\n"
    details_check = True


    for category in categories:
        categories_data.append({
            "photo": category.get("cat_img"),
            "description": category.get("cat_desc"),
            "name": category.get("website category"),
            "business_id": uid,
        })

    category_with_id = {category['name']: category['id'] for category in categories_data}

    services_data = []

    for service in services:
        details_check = False
        services_data.append({
            "business_id":uid,
            "name": service.get("name"),
            "description": service.get("description"),
            "category": service.get("category"),
            "category_id": category_with_id.get(service.get("category")),
        })

    service_with_id = {service['name'] + service['category']: service['id'] for service in services_data}

    service_variations_data = []
    slack_msg_price = "--- Price Missing ---\n"
    slack_msg_duration = "--- Duration Missing ---\n"

    for service in services:
        duration = None if not service.get("duration").isdigit() else int(service.get("duration"))
        price = None if not is_float(service.get("price_start")) else float(service.get("price_start"))
        if not duration:
            details_check = False
            slack_msg_duration += f"Duration missing | {service.get('name')}\n"
        if not price:
            details_check = False
            slack_msg_price += f"Price missing | {service.get('name')}\n"

        service_variations_data.append({
            "service_id": service_with_id.get(service['name'] + service['category']),
            "name": service.get("name"),
            "duration": duration,
            "price": price,
            "description": service.get("description"),
        })

    if details_check:
        await slack.send_slack_message(channel_name, "Service Details added successfully!")
    else:
        await slack.send_slack_message(channel_name, slack_msg + slack_msg_duration + slack_msg_price)

    return {
        "categories": categories_data,
        "services": services_data,
        "service_variations": service_variations_data
    }

