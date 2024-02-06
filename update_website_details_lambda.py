# import secrets

ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "postgres"
REGION = "us-east-1c"
DBNAME = "postgres"
PASS = "March2021"

disc_acc = (
    "https://mybusinessaccountmanagement.googleapis.com/$discovery/rest?version=v1"
)
disc_mybiz = "https://developers.google.com/static/my-business/samples/mybusiness_google_rest_v4p9.json"

import json
import psycopg2
import pandas as pd
import googleapiclient.discovery as gapd
import google.oauth2.credentials
import boto3
from datetime import datetime
import re


def old_sql():
    global conn, cur
    try:
        conn = psycopg2.connect(
            host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS
        )
        cur = conn.cursor()
        print("Loaded creds from hard coded values")
    except Exception as e:
        print("old sql ERROR", e)


def sql():
    global conn, cur
    try:
        conn = psycopg2.connect(
            host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS
        )
        cur = conn.cursor()
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
            )
            query += "'" + val + "'"
        elif type(val) == dict:
            dict_val = (
                json.dumps(val).replace("''", "'").replace("'", "''")
            )
            query += "'" + dict_val + "'"
        elif type(val) == list:
            list_val = (
                json.dumps(val).replace("''", "'").replace("'", "''")
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


def get_gapd_creds(email):
    sql_query("SELECT oauth FROM gmb_oauth WHERE email='" + email + "'")
    res = cur.fetchall()
    creds = json.loads(res[0][0])
    credentials = google.oauth2.credentials.Credentials(**creds)
    return credentials


def get_mybiz_client(credentials):
    try:
        my_biz_client = gapd.build(
            "mybusiness", "v4", credentials=credentials, discoveryServiceUrl=disc_mybiz
        )
        return my_biz_client
    except Exception as e:
        return str(e), 200


def get_biz_info(credentials):
    try:
        biz_acc_client = gapd.build(
            "mybusinessaccountmanagement",
            "v1",
            credentials=credentials,
            discoveryServiceUrl=disc_acc,
        )
        biz_info = biz_acc_client.accounts().list().execute()
        return biz_info
    except Exception as e:
        return str(e), 200


def get_location_db(email):
    sql_query(f"select location from gmb_oauth where email='{email}'")
    location = cur.fetchall()[0][0]
    return location


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


def get_website_details(place_id):
    no_data = []
    place_id = place_id
    try:
        email_q = f"Select email from gmb_biz_data where place_id='{place_id}'"
        sql_query(email_q)
        res = cur.fetchall()
        email = res[0][0]

        credentials = get_gapd_creds(email)
        my_biz_client = get_mybiz_client(credentials)
        biz_info = get_biz_info(credentials)
        location_name = get_location_db(email)
        try:
            reviews = (
                my_biz_client.accounts()
                .locations()
                .reviews()
                .list(
                    parent=f"{biz_info['accounts'][0]['name']}/locations/{location_name}",
                    pageSize=50,
                )
                .execute()
            )
        except Exception as e:
            print(e)
            print(f"Error for {email} in reviews")

        revs = []
        new_review = []
        if "totalReviewCount" in reviews:
            if reviews["totalReviewCount"] > 4:
                i = 0
                while i < 6:
                    for revvs in reviews["reviews"]:
                        if "comment" in revvs.keys():
                            revi = {
                                "id": revvs["reviewId"],
                                "name": revvs["reviewer"]["displayName"],
                                "photo": revvs["reviewer"]["profilePhotoUrl"],
                                "review": revvs["comment"],
                                "star": revvs["starRating"],
                                "date": datetime.fromisoformat(
                                    str(revvs["updateTime"][0:23])
                                )
                                .date()
                                .isoformat(),
                            }
                            revs.append(revi)
                            i += 1

            else:
                for revvs in reviews["reviews"]:
                    if "comment" in revvs.keys():
                        revi = {
                            "id": revvs["reviewId"],
                            "name": revvs["reviewer"]["displayName"],
                            "photo": revvs["reviewer"]["profilePhotoUrl"],
                            "review": revvs["comment"],
                            "star": revvs["starRating"],
                            "date": datetime.fromisoformat(
                                str(revvs["updateTime"][0:23])
                            )
                            .date()
                            .isoformat(),
                        }
                        revs.append(revi)

            review_dict = {}
            for review in revs:
                review_dict[review["id"]] = len(review["review"])
            new_dic = {}
            k = list(review_dict.items())
            k.sort(key=lambda x: x[1], reverse=True)
            for i in k:
                new_dic.update({i[0]: i[1]})
                r = next(item for item in revs if item["id"] == i[0])
                new_review.append(r)

        if len(new_review) == 0:
            no_data.append("Reviews")

        try:
            images = (
                my_biz_client.accounts()
                .locations()
                .media()
                .list(
                    parent=biz_info["accounts"][0]["name"]
                    + "/locations/"
                    + location_name,
                    pageSize=2500,
                )
                .execute()
            )
        except Exception as e:
            print(e)
            print(f"Error for {email}")

        views = []
        if "mediaItems" in images.keys():
            views = []
            for i in images["mediaItems"]:
                if "insights" in i:
                    if "viewCount" in i["insights"]:
                        views.append(int(i["insights"]["viewCount"]))

        views.sort(reverse=True)

        image_list = []
        for v in views[0:30]:
            for i in images["mediaItems"]:
                if "insights" in i:
                    if "viewCount" in i["insights"]:
                        if i["insights"]["viewCount"] == str(v):
                            image_list.append(i)

        imgs = []
        for i in image_list[0:30]:
            url = i["googleUrl"]
            if i["mediaFormat"] == "VIDEO":
                url = i["googleUrl"].replace("=s0", "=dv")
            data = {
                "type": i["mediaFormat"],
                "url": url,
            }
            imgs.append(data)

        if len(imgs) == 0:
            no_data.append("Images")

        # db_query = f"Select * from gmb_profile_details where place_id='{place_id}'"
        db_query = (
            f"select * from gmb_retool_profile_completion where place_id='{place_id}'"
        )
        sql_query(db_query)
        res = cur.fetchall()
        print(f"profile details res len : {len(res[0])}")

        temp_url = " ".join(re.findall("[a-zA-Z]+", res[0][0]))
        biz_url = temp_url.lower().replace(" ", "-")

        biz_name = res[0][0]
        if "'" in biz_name:
            biz_name = res[0][0].replace("'", "''")

        reviewss = json.dumps(new_review[0:6])

        if "'" in reviewss:
            reviewss = reviewss.replace("'", "")

        address = f"{res[0][4]} {res[0][6]} {res[0][7]}, {res[0][5][0:5]}"
        if res[0][4] is None or res[0][4] == "":
            no_data.append("address")

        category = res[0][9]
        number = res[0][1]
        if res[0][1] is None or res[0][1] == "":
            no_data.append("phone number")

        # '''for working hours'''
        workingHours = []
        if res[0][11] != "{}" and res[0][11] != "":
            for hours in json.loads(res[0][11]):
                day = {
                    "day": hours["openDay"],
                    "openTime": hours["openTime"],
                    "closeTime": hours["closeTime"],
                }
                workingHours.append(day)

            weekday = [
                "MONDAY",
                "TUESDAY",
                "WEDNESDAY",
                "THURSDAY",
                "FRIDAY",
                "SATURDAY",
                "SUNDAY",
            ]
            weekday_sort = [
                "MONDAY",
                "TUESDAY",
                "WEDNESDAY",
                "THURSDAY",
                "FRIDAY",
                "SATURDAY",
                "SUNDAY",
            ]
            new_working_hours = []

            for days in workingHours:
                if days["day"] in weekday:
                    weekday.remove(days["day"])
                hours = ""

                if days["closeTime"]["hours"]==24:
                    hours += "Open 24 hours"
                    new_working_hours.append(data)
                    continue

                if days["openTime"]["hours"] == 12:
                    hours += str(days["openTime"]["hours"]) + " PM" + " - "
                elif days["openTime"]["hours"] > 12:
                    hours += str(days["openTime"]["hours"] % 12) + " PM" + " - "
                else:
                    hours += str(days["openTime"]["hours"]) + " AM" + " - "

                if days["closeTime"]["hours"] > 12:
                    hours += str(days["closeTime"]["hours"] % 12) + " PM"
                elif days["closeTime"]["hours"] < 12:
                    hours += str(days["closeTime"]["hours"]) + " PM"
                else:
                    hours += str(days["closeTime"]["hours"]) + " PM"

                data = {"day": days["day"], "hours": hours}
                new_working_hours.append(data)

            for day in weekday:
                data = {"day": day, "hours": "Closed"}
                new_working_hours.append(data)

            new_working_hours = sorted(
                new_working_hours, key=lambda d: weekday_sort.index(d["day"])
            )
            new_working_hours_str = json.dumps(new_working_hours)

        # _______________________________________________
        if new_working_hours_str is None or new_working_hours_str == "":
            no_data.append("Working Hours")

        # ''''for appointment_link'''
        if res[0][13] is not None and res[0][13] != "":
            appointment_link = res[0][13]
        else:
            appointment_link = ""
        if appointment_link is None or appointment_link == "":
            no_data.append("Booking Link")

        submit_text = "SUBMIT" if appointment_link == "" else "Select Services"
        book_text = "Make A Reservation" if appointment_link == "" else "Get in touch"

        gmb_website_status_data = {
            "url": f"https://{biz_url}.chrone.work",
            "place_id": place_id,
            "location": location_name,
            "status": "in_progess",
            "acceptance": None,
            "website_type": "landing_page_v2",
            "old_gmb_website": res[0][3],
        }

        # '''for hero title and description'''
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
                (title_desc_df["category"] == "Default")
                & (title_desc_df["Type"] == "Both")
            ]
            title = row["title"].values[0]
            desc = row["description"].values[0]

        hero_title = row["title"].values[0]
        hero_desc = row["description"].values[0].replace("{biz_name}", biz_name)
        hero_desc = hero_desc.replace("'", "''")

        # '''for services'''
        i = 0
        website_services = []
        services_q = f"select * from user_services where place_id='{place_id}'"
        sql_query(services_q)
        res = cur.fetchall()
        service_cats = []
        for r in res:
            if r[2] not in service_cats:
                service_cats.append(r[2])

        for cat in service_cats:
            data = {
                "website category": cat,
                "cat_img": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/cat_{i}.webp",
                "cat_desc": "Some random description which should be stored in category and description bank.",
                "services": [],
            }
            for r in res:
                if r[2] == cat:
                    price = ""
                    if r[8] == "STARTS_FROM":
                        price = "$" + str(round(r[9])) + "+" if r[9] is not None else ""
                    elif r[8] == "FIXED":
                        price = "$" + str(round(r[9])) if r[9] is not None else ""
                    elif r[8] == "RANGE":
                        price = (
                            "$" + str(round(r[9])) + "-" + "$" + str(round(r[6]))
                            if r[9] is not None
                            else ""
                        )
                    elif r[8] == "NO_PRICE":
                        price = ""
                    data["services"].append(
                        {"name": r[1], "price": price, "description": r[3]}
                    )
            website_services.append(data)
            i += 1
        website_services = json.dumps(website_services)
        website_services = website_services.replace("'", "''")

        sms_number = []
        sms_number.append(number)

        # # update banner image
        # copy_source = {"Bucket": "chrone-website", "Key": "stock/banner.webp"}
        # bucket = s3.Bucket("chrone-website")
        # bucket.copy(copy_source, f"{place_id}/banner.webp")

        # # update services/cat_img image
        # copy_source = {"Bucket": "chrone-website", "Key": "stock/services.webp"}
        # bucket = s3.Bucket("chrone-website")
        # bucket.copy(copy_source, f"{place_id}/services.webp")

        sp_comm_details_query = f"select gbd.place_id,gbd.email,gpd.phone from gmb_biz_data gbd join gmb_profile_details gpd on gpd.place_id=gbd.place_id where gbd.place_id='{place_id}'"
        sql_query(sp_comm_details_query)
        res = cur.fetchall()

        # comm_details_phn = {
        #     "place_id": place_id,
        #     "recipient": get_valid_phone(res[0][2]),
        #     "type": "phone",
        #     "active": "true",
        #     "lead_comm": "true",
        # }

        # comm_details_email = {
        #     "place_id": place_id,
        #     "recipient": res[0][1],
        #     "type": "email",
        #     "active": "true",
        #     "lead_comm": "false",
        # }

        cust_msg = f"Hi! Your booking request with {biz_name} has been received. To make a confirmed booking immediately, you can call us at - {number}"
        if appointment_link is not None and appointment_link != "":
            cust_msg = cust_msg + f" or book by clicking here - {appointment_link}"

        sp_lead_msg_deails = {
            "place_id": place_id,
            "sp_msg": "Cha-Ching!\nYou have a booking request from {cust_type} - {name} on your website.\nPlease call/text them on {phone} immediately to fix an appointment.\n\nCheers,\nTeam Chrone",
            "cust_msg": cust_msg.replace("'", "''"),
            "comm_type": "phone",
        }

        section_data = {
            "root": {"design": {}},
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
                    "description": f"{hero_desc}",
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
            "category": {
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

        section_data_dark = {
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
                    "description": f"{hero_desc}",
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
            "category": {
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

        color_scheme = {
            "primary": {"type": "color", "value": [25, 30, 49], "valueType": "hsl"},
            "secondary": {"type": "color", "value": [25, 30, 49], "valueType": "hsl"},
            "tertiary": {"type": "color", "value": [25, 30, 49], "valueType": "hsl"},
            "textPrimary": {"type": "color", "value": [24, 6, 50], "valueType": "hsl"},
        }

        color_scheme_dark = {
            "primary": {"type": "color", "value": [263, 43, 51], "valueType": "hsl"},
            "secondary": {"type": "color", "value": [263, 43, 51], "valueType": "hsl"},
            "tertiary": {"type": "color", "value": [263, 43, 51], "valueType": "hsl"},
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

        home_section_migrate = [
            {
                "name": "header",
                "path": "landing_page/sections/header/v2.html",
                "type": "header",
            },
            {
                "name": "Home",
                "path": "landing_page/sections/banner/v1.html",
                "type": "banner",
            },
            {
                "name": "Services",
                "path": "landing_page/sections/category/v1.html",
                "type": "category",
            },
            {
                "name": "Working Hours",
                "path": "landing_page/sections/working_hrs/v2.html",
                "type": "working_hrs",
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

        services_section_migrate = [
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

        home_sp_data = {
            "url": biz_url + "-migrate",
            "number": number,
            "place_id": place_id + "-mt",
            "category": category,
            "biz_name": biz_name,
            "address": address,
            "booking_link": appointment_link,
            "working_hours": new_working_hours_str,
            "services_banner": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/services_banner.webp",
            "images": json.dumps(imgs),
            "testimonials": reviewss,
            "title": "Website title",
            "hero_title": hero_title,
            "hero_desc": hero_desc,
            "services": website_services,
            "sms_number": json.dumps(sms_number),
            "book_text": book_text,
            "submit_text": submit_text,
            "banner": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/banner.webp",
            "cat_img": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/services.webp",
            "index_template": "new_template_v2",
            "section_data": section_data,
            "service_template": "service_template",
            "email": email,
            "font_scheme": font_scheme,
            "path": "home",
            "color_scheme": color_scheme,
            "sections": home_section_migrate,
            "base_template": "landing_page/master_v2",
        }
        services_sp_data = {
            "url": biz_url + "-migrate",
            "number": number,
            "place_id": place_id + "-mt",
            "category": category,
            "biz_name": biz_name,
            "address": address,
            "booking_link": appointment_link,
            "working_hours": new_working_hours_str,
            "services_banner": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/services_banner.webp",
            "images": json.dumps(imgs),
            "testimonials": reviewss,
            "title": "Website title",
            "hero_title": hero_title,
            "hero_desc": hero_desc,
            "services": website_services,
            "sms_number": json.dumps(sms_number),
            "book_text": book_text,
            "submit_text": submit_text,
            "banner": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/banner.webp",
            "cat_img": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/services.webp",
            "index_template": "new_template_v2",
            "section_data": section_data,
            "service_template": "service_template",
            "email": email,
            "font_scheme": font_scheme,
            "path": "services",
            "color_scheme": color_scheme,
            "sections": services_section_migrate,
            "base_template": "landing_page/master_v2",
        }

        print(home_sp_data)
        print(services_sp_data)
        status_website_details_home = insert_sql("gmb_website_details", home_sp_data)
        status_website_details_services = insert_sql(
            "gmb_website_details", services_sp_data
        )
        # status_website_status = insert_sql(
        #     "gmb_website_status_new", gmb_website_status_data
        # )
        # status_comms_phone = insert_sql("sp_comm_details", comm_details_phn)
        # status_comms_email = insert_sql("sp_comm_details", comm_details_email)
        # status_lead_comms = insert_sql("lead_comms_dynamic", sp_lead_msg_deails)
        print(biz_url)
        print(f"done for {email}")
        return {
            "status": f"website_details:{status_website_details_home}",
            "status": f"website_details:{status_website_details_services}",
            # "website_status": f"{status_website_status}",
            # "comms_status": f"comms_phn:{status_comms_phone} | comms_email:{status_comms_email}",
            "lead_msg": "{status_lead_comms}",
            "url": f"https://{biz_url}.chrone.work",
        }
    except Exception as e:
        print("Error : ", e)
        return {"status": "error"}


def lambda_handler(event, context):
    # place_id = event["queryStringParameters"]['place_id']
    # print(place_id)
    # ChIJJ9lAl_J1K4cR_SsJRjSa7DA
    # sp_data = get_website_details()
    # sql()
    sp_data = get_website_details("ChIJw2As5MgHK4cR7bBKjoUHW98")
    print(sp_data)
    return {"statusCode": 200, "body": json.dumps(sp_data)}


lambda_handler("", "")
