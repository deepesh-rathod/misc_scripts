ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "postgres"
REGION = "us-east-1c"
DBNAME = "postgres"
PASS = "March2021"

import json
import psycopg2
import pandas as pd
import googleapiclient.discovery as gapd
import google.oauth2.credentials
import boto3
from datetime import datetime
import re
import requests
from psycopg2.extras import RealDictCursor


def old_sql():
    global conn, cur
    try:
        conn = psycopg2.connect(
            host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        print("Loaded creds from hard coded values")
    except Exception as e:
        print("old sql ERROR", e)


def sql():
    global conn, cur
    try:
        conn = psycopg2.connect(
            host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    except Exception as e:
        print("ERROR", e)


old_sql()


def sql_query(query):
    global cur
    try:
        cur.execute(query)
    except:
        sql()
        cur.execute(query)


def insert_sql(table, data):
    query = "insert into " + table + "("
    keys = list(data.keys())
    query += ", ".join(keys) + ") values ("
    itr = 0
    for key in keys:
        itr += 1
        val = data[key]
        if type(val) == str:
            val = (
                val.replace("''", "'")
                .replace("'", "''")
                .replace("%%", "%")
                .replace("%", "%%")
            )
            query += "'" + val + "'"
        elif type(val) == dict:
            dict_val = (
                json.dumps(val)
                .replace("''", "'")
                .replace("'", "''")
                .replace("%%", "%")
                .replace("%", "%%")
            )
            query += "'" + dict_val + "'"
        elif type(val) == list:
            list_val = (
                json.dumps(val)
                .replace("''", "'")
                .replace("'", "''")
                .replace("%%", "%")
                .replace("%", "%%")
            )
            query += "'" + list_val + "'"
        elif type(val) == int:
            query += str(val)
        elif type(val) == float:
            query += str(val)
        elif type(val) == bool:
            if val:
                query += "true"
            else:
                query += "false"
        elif val is None:
            query += "null"
        if itr == len(keys):
            query += ")"
        else:
            query += ", "
    try:
        sql_query(query)
        conn.commit()
        return "Success"
    except Exception as e:
        return str(e)


session = boto3.Session(
    aws_access_key_id="AKIASQ6IOBTRNZ2TKNHO",
    aws_secret_access_key="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",
)
s3 = session.resource("s3")


def get_valid_phone(phone_number):
    digits = re.findall(r"\d", phone_number)[-10:]
    if len(digits):
        return "".join(digits)
    else:
        return None


def get_reviews(place_id, email):
    api_resp = requests.get(
        f"https://chrone.work/get-reviews?email={email}&place_id={place_id}"
    )
    reviews = json.loads(api_resp.text)
    return reviews


def get_biz_details(place_id):
    db_query = (
        f"select * from gmb_retool_profile_completion where place_id='{place_id}'"
    )
    sql_query(db_query)
    res = cur.fetchall()
    return dict(res[0])


def get_website_services(place_id):
    website_services = []
    services_q = f"select * from user_services where place_id='{place_id}'"
    sql_query(services_q)
    response = cur.fetchall()
    res = []
    for r in response:
        res.append(dict(r))

    service_cats = []
    for r in res:
        if r["category"] not in service_cats:
            service_cats.append(dict(r)["category"])

    i = 0
    for cat in service_cats:
        data = {
            "website category": cat,
            "cat_img": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/cat_{i}.webp",
            "cat_desc": "Some random description which should be stored in category and description bank.",
            "services": [],
        }
        for r in res:
            if r["category"].replace("\n", "") == cat:
                price = ""
                if r["pricing_type"] == "STARTS_FROM":
                    price = (
                        "$" + str(round(r["price_start"])) + "+"
                        if r["price_end"] is not None
                        else ""
                    )
                elif r["pricing_type"] == "FIXED":
                    price = (
                        "$" + str(round(r["price_start"]))
                        if r["price_end"] is not None
                        else ""
                    )
                elif r["pricing_type"] == "RANGE":
                    price = (
                        "$"
                        + str(round(r["price_start"]))
                        + "-"
                        + "$"
                        + str(round(r["price_start"]))
                        if r["price_end"] is not None
                        else ""
                    )
                elif r["pricing_type"] == "NO_PRICE":
                    price = ""
                data["services"].append(
                    {"name": r["name"], "price": price, "description": r["description"]}
                )
        website_services.append(data)
        i += 1

    return website_services


def get_sp_comm_details(place_id):
    sp_comm_details_query = f"select gbd.place_id,gbd.email,gpd.phone from gmb_biz_data gbd join gmb_profile_details gpd on gpd.place_id=gbd.place_id where gbd.place_id='{place_id}'"
    sql_query(sp_comm_details_query)
    response = cur.fetchall()
    res = dict(response[0])

    data_phn = {
        "place_id": place_id,
        "recipient": get_valid_phone(res["phone"]),
        "type": "phone",
        "active": "true",
        "lead_comm": "true",
    }

    data_email = {
        "place_id": place_id,
        "recipient": res["email"],
        "type": "email",
        "active": "true",
        "lead_comm": "false",
    }

    return data_phn, data_email


def get_lead_comms_details(appointment_link, biz_name, place_id, number):
    cust_msg = f"Hi! Your booking request with {biz_name} has been received. To make a confirmed booking immediately, you can call us at - {number}"
    if appointment_link is not None and appointment_link != "":
        cust_msg = cust_msg + f" or book by clicking here - {appointment_link}"

    data = {
        "place_id": place_id,
        "sp_msg": "Cha-Ching!\nYou have a booking request from {cust_type} - {name} on your website.\nPlease call/text them on {phone} immediately to fix an appointment.\n\nCheers,\nTeam Chrone",
        "cust_msg": cust_msg.replace("'", "''"),
        "comm_type": "phone",
    }

    return data


def get_hero_title_description(category, biz_name):
    sheet_id = "1mYZDaK1SVjNukN83vsnvu8P913OD1djWRl-2OsJ8xak"
    sheet_name = "title_desc"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    title_desc_df = pd.read_csv(url)

    row = title_desc_df.loc[
        (title_desc_df["category"] == category) & (title_desc_df["Type"] == "Team")
    ]
    try:
        title = row["title"].values[0]
        desc = row["description"].values[0]
    except:
        row = title_desc_df.loc[
            (title_desc_df["category"] == "Default") & (title_desc_df["Type"] == "Both")
        ]
        title = row["title"].values[0]
        desc = row["description"].values[0]

    hero_title = row["title"].values[0]
    hero_desc = row["description"].values[0].replace("{biz_name}", biz_name)

    return hero_title, hero_desc


def get_email(place_id):
    email_q = f"Select email from gmb_biz_data where place_id='{place_id}'"
    sql_query(email_q)
    res = cur.fetchall()
    data = dict(res[0])
    return data["email"]


def get_section_data(place_id, book_text, hero_title, hero_description):
    section_data = {
        "root": {
            "design": {
                "color": {
                    "body": "--color-text-P0",
                    "section_heading": "--color-text-P90",
                    "section_description": "--color-text-P90",
                }
            }
        },
        "banner": {
            "design": {},
            "content": {
                "media": [
                    {
                        "url": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/banner.webp",
                        "type": "PHOTO",
                    },
                    {"url": "null", "type": "PHOTO"},
                ],
                "title": f"{hero_title}",
                "description": f"{hero_description}",
            },
        },
        "gallery": {
            "design": {},
            "content": {
                "media": [],
                "title": "Gallery",
                "description": "Get a glimpse of our services with our inspiring gallery of images.",
            },
        },
        "services": {
            "design": {},
            "content": {
                "title": "Services",
                "description": "We offer a full range of high-end, top-quality services using the best beauty products and styling.",
            },
        },
        "working_hrs": {
            "design": {},
            "content": {
                "media": [
                    {
                        "url": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/services.webp",
                        "type": "PHOTO",
                    }
                ],
                "title": "What we do",
                "description": "We offer a full range of high-end, top-quality services using the best beauty products and styling.",
            },
        },
        "contact_form": {
            "design": {},
            "content": {
                "title": book_text,
                "description": "Book your appointment now by filling in the following details",
            },
        },
        "testimonials": {
            "design": {},
            "content": {
                "title": "Testimonials",
                "description": "Hear from our best customers, sharing their experiences with us!",
            },
        },
    }

    return section_data


def get_scheme_variables(theme):
    color_scheme = {
        "primary": {"type": "color", "value": [25, 30, 49], "valueType": "hsl"},
        "secondary": {"type": "color", "value": [25, 30, 49], "valueType": "hsl"},
        "tertiary": {"type": "color", "value": [25, 30, 49], "valueType": "hsl"},
        "textPrimary": {"type": "color", "value": [24, 6, 50], "valueType": "hsl"},
    }

    font_scheme = {
        "body_font": {
            "link": "https://fonts.googleapis.com/css?family=Playfair%20Display",
            "name": "Playfair Display",
            "family": "serif",
        },
        "head_font": {
            "link": "https://fonts.googleapis.com/css?family=Josefin%20Sans",
            "name": "Josefin Sans",
            "family": "sans-serif",
        },
    }

    services_sections = [
        {
            "name": "header",
            "path": "landing_page/sections/header/v1.html",
            "type": "header",
        },
        {
            "name": "Home",
            "path": "landing_page/sections/banner/v3.html",
            "type": "banner",
        },
        {
            "name": "Services",
            "path": "landing_page/sections/services/v1.html",
            "type": "services",
        },
        {
            "name": "Contact Us",
            "path": "landing_page/sections/contact_form/v2.html",
            "type": "contact_form",
        },
        {
            "name": "FAB",
            "path": "landing_page/sections/fab_mobile/v2.html",
            "type": "fab_mobile",
        },
        {
            "name": "footer",
            "path": "landing_page/sections/footer/v1.html",
            "type": "footer",
        },
    ]

    home_sections = [
        {
            "name": "header",
            "path": "landing_page/sections/header/v2.html",
            "type": "header",
        },
        {
            "name": "Home",
            "path": "landing_page/sections/banner/v2.html",
            "type": "banner",
        },
        {
            "name": "About Us",
            "path": "landing_page/sections/working_hrs/v2.html",
            "type": "working_hrs",
        },
        {
            "name": "Services",
            "path": "landing_page/sections/category/v2.html",
            "type": "category",
        },
        {
            "name": "Gallery",
            "path": "landing_page/sections/gallery/v2.html",
            "type": "gallery",
        },
        {
            "name": "Testimonials",
            "path": "landing_page/sections/testimonials/v2.html",
            "type": "testimonials",
        },
        {
            "name": "Contact Us",
            "path": "landing_page/sections/contact_form/v2.html",
            "type": "contact_form",
        },
        {
            "name": "FAB",
            "path": "landing_page/sections/fab_mobile/v2.html",
            "type": "fab_mobile",
        },
        {
            "name": "footer",
            "path": "landing_page/sections/footer/v2_1.html",
            "type": "footer",
        },
    ]

    color_scheme_dark = {
        "primary": {"type": "color", "value": [263, 43, 51], "valueType": "hsl"},
        "secondary": {"type": "color", "value": [263, 43, 51], "valueType": "hsl"},
        "tertiary": {"type": "color", "value": [263, 43, 51], "valueType": "hsl"},
        "textPrimary": {"type": "color", "value": [24, 6, 50], "valueType": "hsl"},
    }

    services_sections_dark = [
        {
            "name": "header",
            "path": "landing_page/sections/header/v5.html",
            "type": "header",
        },
        {
            "name": "Home",
            "path": "landing_page/sections/banner/v3.html",
            "type": "banner",
        },
        {
            "name": "Services",
            "path": "landing_page/sections/services/v2.html",
            "type": "services",
        },
        {
            "name": "Contact Us",
            "path": "landing_page/sections/contact_form/v1.html",
            "type": "contact_form",
        },
        {
            "name": "FAB",
            "path": "landing_page/sections/fab_mobile/v1.html",
            "type": "fab_mobile",
        },
        {
            "name": "footer",
            "path": "landing_page/sections/footer/v4.html",
            "type": "footer",
        },
    ]

    home_sections_dark = [
        {
            "name": "header",
            "path": "landing_page/sections/header/v5.html",
            "type": "header",
        },
        {
            "name": "Home",
            "path": "landing_page/sections/banner/v1.html",
            "type": "banner",
        },
        {
            "name": "Services",
            "path": "landing_page/sections/category/v3.html",
            "type": "category",
        },
        {
            "name": "About Us",
            "path": "landing_page/sections/working_hrs/v1.html",
            "type": "working_hrs",
        },
        {
            "name": "Gallery",
            "path": "landing_page/sections/gallery/v1.html",
            "type": "gallery",
        },
        {
            "name": "Testimonials",
            "path": "landing_page/sections/testimonials/v1.html",
            "type": "testimonials",
        },
        {
            "name": "Contact Us",
            "path": "landing_page/sections/contact_form/v1.html",
            "type": "contact_form",
        },
        {
            "name": "FAB",
            "path": "landing_page/sections/fab_mobile/v1.html",
            "type": "fab_mobile",
        },
        {
            "name": "footer",
            "path": "landing_page/sections/footer/v4.html",
            "type": "footer",
        },
    ]

    if theme == "light":
        return font_scheme, color_scheme, home_sections, services_sections

    if theme == "dark":
        return (
            font_scheme,
            color_scheme_dark,
            home_sections_dark,
            services_sections_dark,
        )


def create_website(place_id):
    email = get_email(place_id)

    reviews = get_reviews(place_id, email)["reviews"]

    ratings = ["ONE", "TWO", "THREE", "FOUR", "FIVE"]
    reviews = sorted(
        reviews, key=lambda review: ratings.index(review["starRating"]), reverse=True
    )
    website_reviews = json.dumps(reviews).replace("'", "''")

    services = get_website_services(place_id)
    website_services = json.dumps(services).replace("'", "''")

    biz_details = get_biz_details(place_id)
    biz_name = biz_details["title"]
    address = f"{biz_details['address']} {biz_details['city']} {biz_details['state']}, {biz_details['zipcode'][0:5]}"
    number = biz_details["phone"]

    workingHours = []
    if biz_details["regularHours"] != "{}" and biz_details["regularHours"] != "":
        for hours in json.loads(biz_details["regularHours"]):
            day = {
                "day": hours["openDay"],
                "openTime": hours["openTime"],
                "closeTime": hours["closeTime"],
            }
            workingHours.append(day)

    appointment_link = (
        biz_details["appointmentLink"]
        if biz_details["appointmentLink"] is not None
        else ""
    )

    submit_text = "SUBMIT" if appointment_link == "" else "Select Services"
    book_text = "Make A Reservation" if appointment_link == "" else "Get in touch"

    temp_url = " ".join(re.findall("[a-zA-Z]+", biz_name))
    biz_url = temp_url.lower().replace(" ", "-")

    hero_title, hero_description = get_hero_title_description(
        biz_details["primaryCategories"], biz_name
    )

    section_data = get_section_data(place_id, book_text, hero_title, hero_description)

    font_scheme, color_scheme, home_sections, service_sections = get_scheme_variables(
        "light"
    )

    comm_details_phn,comm_details_email=get_sp_comm_details(place_id)
    sp_lead_msg_deails = get_lead_comms_details(place_id,biz_name,place_id,number)

    home_sp_data = {
        "url": biz_url,
        "number": number,
        "place_id": place_id,
        "biz_name": biz_name,
        "address": address,
        "booking_link": appointment_link,
        "working_hours": json.dumps(workingHours),
        "services_banner": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/services_banner.webp",
        "testimonials": website_reviews,
        "title": "Website title",
        "hero_title": hero_title,
        "hero_desc": hero_description,
        "services": website_services,
        "book_text": book_text,
        "submit_text": submit_text,
        "index_template": "new_template_v2",
        "section_data": section_data,
        "service_template": "service_template",
        "email": email,
        "font_scheme": font_scheme,
        "path": "home",
        "color_scheme": color_scheme,
        "sections": home_sections,
        "base_template": "landing_page/master_v1",
    }

    services_sp_data = {
        "url": biz_url,
        "number": number,
        "place_id": place_id,
        "biz_name": biz_name,
        "address": address,
        "booking_link": appointment_link,
        "working_hours": json.dumps(workingHours),
        "services_banner": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/services_banner.webp",
        "testimonials": website_reviews,
        "title": "Website title",
        "hero_title": hero_title,
        "hero_desc": hero_description,
        "services": website_services,
        "book_text": book_text,
        "submit_text": submit_text,
        "index_template": "new_template_v2",
        "section_data": section_data,
        "service_template": "service_template",
        "email": email,
        "font_scheme": font_scheme,
        "path": "home",
        "color_scheme": color_scheme,
        "sections": service_sections,
        "base_template": "landing_page/master_v1",
    }

    gmb_website_status_data = {
        "url": f"https://{biz_url}.chrone.work",
        "place_id": place_id,
        "location": location_name,
        "status": "in_progess",
        "acceptance": None,
        "website_type": "landing_page_v2",
        "old_gmb_website": biz_details['website'],
    }

    status_website_details_home = insert_sql("gmb_website_details", home_sp_data)
    status_website_details_services = insert_sql(
        "gmb_website_details", services_sp_data
    )
    status_website_status = insert_sql(
        "gmb_website_status_new", gmb_website_status_data
    )
    status_comms_phone = insert_sql("sp_comm_details", comm_details_phn)
    status_comms_email = insert_sql("sp_comm_details", comm_details_email)
    status_lead_comms = insert_sql("lead_comms_dynamic", sp_lead_msg_deails)

    print(0)


create_website("")
