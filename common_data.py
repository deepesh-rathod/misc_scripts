import os
import json
import google.oauth2.credentials
import google_auth_oauthlib
import googleapiclient.discovery as gapd
from datetime import time, timedelta
import uuid
from requests import request
import re
import ast

ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "postgres"
REGION = "us-east-1c"
DBNAME = "postgres"
PASS = "March2021"
SECRET = "04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c"

import psycopg2
import psycopg2.extras
import pandas as pd
from datetime import datetime, date, timedelta


def sql():
    global conn, cur
    try:
        conn = psycopg2.connect(
            host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS
        )
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    except Exception as e:
        print("ERROR", e)


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
            query += "'" + val + "'"
        elif type(val) == dict:
            query += "'" + json.dumps(val) + "'"
        elif type(val) == list:
            query += "'" + json.dumps(val) + "'"
        elif type(val) == int:
            query += str(val)
        elif type(val) == float:
            query += str(val)
        elif type(val) == bool:
            query += str(val)
        elif val is None:
            query += "NULL"
        if itr == len(keys):
            query += ")"
        else:
            query += ", "
    try:
        sql_query(query)
        conn.commit()
        return "Success"
    except Exception as e:
        print(e)
        return str(e)


def update_sql(table, data, update_filter):
    query = "update " + table + " set "
    itr = 0
    for key in data.keys():
        itr += 1
        val = data[key]
        if type(val) == str:
            val = (
                val.replace("''", "'")
                .replace("'", "''")
                .replace("%%", "%")
                .replace("%", "%%")
            )
            query += key + "='" + val + "'"
        elif type(val) == dict:
            dict_val = (
                json.dumps(val)
                .replace("''", "'")
                .replace("'", "''")
                .replace("%%", "%")
                .replace("%", "%%")
            )
            query += key + "='" + dict_val + "'"
        elif type(val) == list:
            list_val = (
                json.dumps(val)
                .replace("''", "'")
                .replace("'", "''")
                .replace("%%", "%")
                .replace("%", "%%")
            )
            query += key + "='" + list_val + "'"
        elif type(val) == int:
            query += key + "=" + str(val)
        elif type(val) == float:
            query += key + "=" + str(val)
        elif type(val) == bool:
            if val:
                query += key + "=" + "true"
            else:
                query += key + "=" + "false"
        elif val is None:
            query += key + "=" + "NULL"
        if itr == len(data.keys()):
            pass
        else:
            query += ", "

    query += f"{update_filter}"
    try:
        sql_query(query)
        conn.commit()
        return "Success"
    except Exception as e:
        return str(e)
    
def bulk_update_table(table, primary_key, data):    
    col_str = ""
    col_list_str = ""
    column_names = data[0].keys()
    
    for i, col in enumerate(column_names):
        if col != primary_key:
            print(col)
            if i==len(column_names)-1:
                col_str += f"{col} = c.{col}"
            else:
                col_str += f"{col} = c.{col}, "
        if i==len(column_names)-1:
            col_list_str += f"{col}"
        else:
            col_list_str += f"{col}, "
    
    master_values = ""
    for j, data_json in enumerate(data):
        value_tup = "("
        for ind, key in enumerate(data_json.keys()):
            if type(data_json[key])==str:
                data_value = f"'{data_json[key]}'"
            else:
                data_value = data_json[key]
            if ind==len(data_json.keys())-1:
                value_tup += str(data_value) if type(data_value)==int else "'" + str(data_value).replace("'",'"') + "'::jsonb"
            else:
                value_tup += f"{data_value}, " if type(data_value)==int else "'" + str(data_value).replace("'",'"') + "'::jsonb"
        value_tup += ")"

        if j==len(data)-1:
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


update_data = {
    "url": "twinn-touch",
    "place_id": "ChIJzVZ2FmWp2YgRoZhP2sNO7OQ",
    "category": None,
    "biz_name": "Twinn Touch",
    "address": "Suite #1, 4415 Hollywood Blvd, Hollywood FL, 33021",
    "logo_link": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/img_placeholder.webp",
    "working_hours": "[{\"day\": \"MONDAY\", \"hours\": \"Closed\"}, {\"day\": \"TUESDAY\", \"hours\": \"10 AM - 7 PM\"}, {\"day\": \"WEDNESDAY\", \"hours\": \"10 AM - 7 PM\"}, {\"day\": \"THURSDAY\", \"hours\": \"10 AM - 7 PM\"}, {\"day\": \"FRIDAY\", \"hours\": \"10 AM - 7 PM\"}, {\"day\": \"SATURDAY\", \"hours\": \"9 AM - 6 PM\"}, {\"day\": \"SUNDAY\", \"hours\": \"Closed\"}]",
    "services_banner": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/services_banner.webp",
    "number": "(786) 496-0783",
    "biz_desc": None,
    "services": "[{\"website category\": \"Natural Nails\", \"cat_img\": \"https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/naturalnails.webp\", \"cat_desc\": \"Enhance your natural beauty with impeccably manicured nails that exude elegance and grace.\", \"services\": [{\"name\": \"Luminary nail repair\", \"price\": \"$7\", \"description\": \"\"}, {\"name\": \"Soak off\", \"price\": \"$10\", \"description\": \"\"}, {\"name\": \"Luminary\", \"price\": \"$65\", \"description\": \"-Multi Flex Gel - Luminary is a structure manicure that's designed to help strengthen your natural nails and improve their overall health. - Can help reduce nail breakage and promote healthy growth, which means you can enjoy longer, stronger nails that look great.\"}, {\"name\": \"Gel Manicure\", \"price\": \"$35\", \"description\": \"\"}, {\"name\": \"Manicure\", \"price\": \"$20\", \"description\": \"\"}, {\"name\": \"Gel polish change on hands\", \"price\": \"$30\", \"description\": \"\"}, {\"name\": \"Hard gel\", \"price\": \"$80\", \"description\": \"\"}]}, {\"website category\": \"Apres Gel X\", \"cat_img\": \"https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/apresgelx.webp\", \"cat_desc\": \"Enhance your nails with a flawless and long-lasting finish using our innovative gel extension system.\", \"services\": [{\"name\": \"Apres Gel X\", \"price\": \"$60\", \"description\": \"Extensions that come in different shapes from coffin, square, stiletto, and almond and lengths from short to long. It can last up to 3 to 4 weeks.\"}, {\"name\": \"Apres Gel X w. Soak off\", \"price\": \"$70\", \"description\": \"\"}, {\"name\": \"Gel X Repair\", \"price\": \"$5\", \"description\": \"\"}]}, {\"website category\": \"Eyebrows\", \"cat_img\": \"https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/eyebrows.webp\", \"cat_desc\": \"Enhance your facial features with perfectly groomed and defined eyebrows, framing your face beautifully.\", \"services\": [{\"name\": \"Brow Wax\", \"price\": \"$10\", \"description\": \"\"}]}, {\"website category\": \"Facials\", \"cat_img\": \"https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/facials.webp\", \"cat_desc\": \"Revitalize your skin and reveal a radiant glow with our rejuvenating facial treatments.\", \"services\": [{\"name\": \"Essential Facial\", \"price\": \"$100\", \"description\": \"The Basic facial . Doesn\\u2019t include extractions. If you would like to include extractions, facial massage , or neck & arm massage please select the options under add on's .\"}, {\"name\": \"Masculine Facial\", \"price\": \"$110\", \"description\": \"This facial is specifically for Men . If you would like a facial massage or neck & arm massage please select option under add on's .\"}, {\"name\": \"Dermaplaning Facial\", \"price\": \"$130\", \"description\": \"Dermaplaning removes the top layer of the skin . This is a form of exfoliation with a use of a scalpel.\"}, {\"name\": \"Shine Bright Facial\", \"price\": \"$115\", \"description\": \"Focusing on skin brightness. Targeted to get rid of hyperpigmentation (dark spots).\"}, {\"name\": \"Pop-Me Facial\", \"price\": \"$120\", \"description\": \"Targeted for acne prone skin . Focusing on taming acne pimples and congestion.\"}, {\"name\": \"Teen Facial\", \"price\": \"$90\", \"description\": \"For teens 13-17 yrs old\"}]}, {\"website category\": \"Masculine Facial\", \"cat_img\": \"https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/masculinefacial.webp\", \"cat_desc\": \"\\nRevitalize your appearance with our specialized facial treatment tailored for masculine needs.\", \"services\": [{\"name\": \"Father's Spa Day\", \"price\": \"$90\", \"description\": \"A masculine facial for our father's on a special day. Comes with a complimentary shoulder massage.\"}]}, {\"website category\": \"Foot Care\", \"cat_img\": \"https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/footcare.webp\", \"cat_desc\": \"Pamper your feet with our expert foot care treatments, providing ultimate comfort and rejuvenation.\", \"services\": [{\"name\": \"Pedicure\", \"price\": \"$40\", \"description\": \"\"}, {\"name\": \"Spa Pedicure\", \"price\": \"$55\", \"description\": \"A regular pedi with an addition of a mask and hot towels to your service\"}, {\"name\": \"Gel Pedicure\", \"price\": \"$55\", \"description\": \"\"}, {\"name\": \"Gold Pedicure\", \"price\": \"$65\", \"description\": \"\"}, {\"name\": \"Reg. Polish Change- Feet\", \"price\": \"$15\", \"description\": \"\"}, {\"name\": \"Gel Polish Change- Feet\", \"price\": \"$25\", \"description\": \"\"}]}, {\"website category\": \"Lashes\", \"cat_img\": \"https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/lashes.webp\", \"cat_desc\": \"Enhance your natural beauty with stunning and voluminous lashes that captivate.\", \"services\": [{\"name\": \"Classic Lash Fullset\", \"price\": \"$90\", \"description\": \"Classic lash full set is a 1 to 1 ratio: 1 extension to 1 natural lash of any type of style that best fits your eye shape . Last 2-3 weeks. If you already have a full lash line of healthy lashes and just want more Umph this is for you.\"}, {\"name\": \"Hybrid Lash Fullset\", \"price\": \"$100\", \"description\": \"Hybrid lash full set is a mix between classic lashes ( 1 extension to 1 individual natural lash) and volume lashes (multiple extensions to 1 individual natural lash). Last 2-3 weeks. This look is for people with few natural lashes that want a fuller look.\"}, {\"name\": \"Volume Lash Fullset\", \"price\": \"$120\", \"description\": \"Volume lash full set is multiple extensions to 1 natural lash. Last 2-3 weeks. If you have very few natural lashes and want a dramatic look this is for you.\"}, {\"name\": \"Classic Lash Refill\", \"price\": \"$60\", \"description\": \"2-3 weeks after fullset with 50% or more lash extensions to give you back your full look . If you don't have 50% or more of lash extensions on or it is past 2-3 weeks, please schedule a fullset so there is more time to fill in your lashes.\"}, {\"name\": \"Hybrid Lash Refill\", \"price\": \"$80\", \"description\": \"2-3 weeks after fullset with 50% or more lash extensions to give you back your full look . If you don't have 50% or more of lash extensions on or it is past 2-3 weeks, please schedule a fullset so there is more time to fill in your lashes.\"}, {\"name\": \"Volume Lash Refill\", \"price\": \"$95\", \"description\": \"2-3 weeks after fullset with 50% or more lash extensions to give you back your full look . If you don't have 50% or more of lash extensions on or it is past 2-3 weeks please schedule a fullset so there is more time to fill in your lashes.\"}, {\"name\": \"Mega Volume Fullset\", \"price\": \"$150\", \"description\": \"Mega Volume lash full set is multiple extensions to 1 natural lash. Last 2-3 weeks. If you want a very full Lash Line this look is for you.\"}, {\"name\": \"Mega Volume Refill\", \"price\": \"$110\", \"description\": \"2-3 weeks after fullset with 50% or more lash extensions to give you back your full look . If you don't have 50% or more of lash extensions on or it is past 2-3 weeks please schedule a fullset so there is more time to fill in your lashes.\"}, {\"name\": \"Lash Removal\", \"price\": \"$20\", \"description\": \"\"}, {\"name\": \"TOUCH UP\", \"price\": \"$50\", \"description\": \"Classis, Hybrid, Volume, Mega Volume touch ups are done within 7 days of initial service (your last fullset or refill). CAN NOT SCHEDULE PAST THE 7TH DAY FOR A TOUCH UP .\"}]}, {\"website category\": \"Nail Design\", \"cat_img\": \"https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/naildesign.webp\", \"cat_desc\": \"Express your unique style with stunning and artistic nail designs that make a statement.\", \"services\": [{\"name\": \"Intricate\", \"price\": \"$45\", \"description\": \"\"}, {\"name\": \"Chrome\", \"price\": \"$20\", \"description\": \"\"}, {\"name\": \"French\", \"price\": \"$30\", \"description\": \"\"}]}, {\"website category\": \"Lash Training\", \"cat_img\": \"https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/lashtraining.webp\", \"cat_desc\": \"Master the art of stunning lashes with our comprehensive and professional lash training program.\", \"services\": [{\"name\": \"Lash Training\", \"price\": \"$550\", \"description\": \"-\"}]}]",
    "testimonials": "[{\"id\": \"AbFvOql3RRT3Oy2JNmaTNB1rHaVn_9YBOw3xYuf-VLr_0NcT-miTnwtpmnc2oM-P0xS6T8HxhKJPgA\", \"name\": \"Hansle L\", \"photo\": \"https://lh3.googleusercontent.com/a-/AD_cMMQkEZDFpIm0eEg7BTMA-hbY6iL_TN2YvqVta4Nvq7vuu9x8=s120-c-rp-mo-br100\", \"review\": \"A loyal customer\", \"star\": \"FIVE\", \"date\": \"Sat, 15 Jul, 2023\"}, {\"id\": \"AbFvOqk_MnijFok2JjjMRliEIIAahwyAFIAyJu1l_dauIlil4fsphaFEV1N8PwUt8h5aYGogR1agUQ\", \"name\": \"Georgena Riviere\", \"photo\": \"https://lh3.googleusercontent.com/a/AAcHTtcyEl5GCKDQvkkGH4QEFbx0-g6PgqzFO1Q1lguv7eTJ=s120-c-rp-mo-br100\", \"review\": \"I've been getting my nails done by Alexis for a couple years now. She's very professional and is a perfectionist. I'm in love with my nails every time I leave.\", \"star\": \"FIVE\", \"date\": \"Fri, 30 Jun, 2023\"}, {\"id\": \"AbFvOqlEjnT1hf7C3exPBAfL20DeIDBTP0GRyftNW4OVI7FzVeagQ4j0CJkwBCNKFtL3jh3OXjTqgQ\", \"name\": \"TasiTas\", \"photo\": \"https://lh3.googleusercontent.com/a-/AD_cMMS7SypXXo6fjFNcJPlD29lrFJ6_7eXeJcbiGUvJH-kqJ-mJ=s120-c-rp-mo-br100\", \"review\": \"Thanks to Alexis for really taking her craft seriously and always providing quality results. I\\u2019ve been a client for a good while now and she never disappoints.\", \"star\": \"FIVE\", \"date\": \"Sun, 25 Jun, 2023\"}]",
    "images": None,
    "title": "Website title",
    "booking_link": "https://twinntouch.as.me/schedule.php",
    "index_template": "new_template_v2",
    "cat_img": None,
    "banner": None,
    "hero_title": "For your beautiful brows and lashes",
    "hero_desc": "Welcome to Twinn Touch, where we offer personalized eyelash treatments to meet your individual needs and goals. Whether you're looking for lash extensions, lifts, tinting, perming or shaping, we have the experience and expertise to help you look and feel your best.",
    "book_text": "Book Appointment",
    "sms_number": None,
    "banner_phn": None,
    "submit_text": "Select Services",
    "section_data": {
        "root": {
            "design": {
                "color": {
                    "body": "--color-P90",
                    "section_heading": "--color-text-P10",
                    "section_description": "--color-text-P10"
                }
            }
        },
        "banner": {
            "design": {
                "color": {
                    "hero_title_text": "--color-text-P0",
                    "reservation_btn_text": "--color-text-P100",
                    "hero_description_text": "--color-text-P0",
                    "reservation_btn_background": "--color-P50",
                    "hero_title_description_container": "--color-text-P100"
                }
            },
            "content": {
                "media": [
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/banner.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "None",
                        "type": "PHOTO"
                    }
                ],
                "title": "Twinn Touch: Beauty in Harmony",
                "description": "Twinn Touch fuses nail artistry and beauty care to cultivate a symphony of elegance. Here, personal style meets expert technique, transforming each appointment into an experience of indulgence. Step into a world where beauty meets sophistication at Twinn Touch."
            }
        },
        "footer": {
            "design": {
                "color": {
                    "text": "--color-text-P100",
                    "background": "--color-P10",
                    "anchor_text": "--color-text-P100"
                }
            }
        },
        "header": {
            "design": {},
            "content": {
                "header_links": [
                    {
                        "link": "banner",
                        "name": "Home"
                    },
                    {
                        "link": "working_hrs",
                        "name": "About Us"
                    },
                    {
                        "link": "category",
                        "name": "Services"
                    },
                    {
                        "link": "gallery",
                        "name": "Gallery"
                    },
                    {
                        "link": "testimonials",
                        "name": "Testimonials"
                    }
                ]
            }
        },
        "gallery": {
            "design": {
                "color": {
                    "img_border_color": "--color-text-P100"
                }
            },
            "content": {
                "media": [
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/9.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/0.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/1.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/2.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/10.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/8.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/3.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/4.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/13.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/5.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/6.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/7.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/17.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/11.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/12.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/14.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/15.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/gallery/16.webp",
                        "type": "PHOTO"
                    }
                ],
                "title": "Gallery",
                "description": "Get a glimpse of my services with an inspiring gallery of images."
            }
        },
        "socials": [
            {
                "id": "TwinnTouch Inc.",
                "link": "https://www.instagram.com/twinntouch",
                "logo": "https://d15e7bk5l2jbs8.cloudfront.net/ph_instagram-logo.png",
                "type": "insta"
            }
        ],
        "category": {
            "design": {
                "color": {
                    "cta_text": "--color-S50",
                    "cta_border": "--color-S80",
                    "title_text": "--color-text-P10",
                    "arrow_border": "--color-text-P100",
                    "cta_text_hover": "--color-text-P100",
                    "arrow_background": "--color-text-P50",
                    "cta_border_hover": "--color-S50",
                    "description_text": "--color-text-P10",
                    "section_description": "--color-text-P100",
                    "cta_background_hover": "--color-P50",
                    "arrow_background_hover": "--color-P50"
                }
            },
            "content": {
                "title": "Services",
                "description": "Experience a full range of high-end, top-quality services using the best beauty products and styling."
            }
        },
        "fab_mobile": {
            "design": {
                "color": {
                    "cta_text": "--color-text-P100",
                    "background": "--color-P90",
                    "cta_background": "--color-P50",
                    "cta_hover_background": "--color-P30"
                }
            }
        },
        "working_hrs": {
            "design": {
                "color": {
                    "text": "--color-text-P100",
                    "phone_email": "--color-text-80",
                    "social_text": "--color-text-P100",
                    "address_hours": "--color-text-80",
                    "phone_email_hover": "--color-text-80"
                }
            },
            "content": {
                "media": [
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJzVZ2FmWp2YgRoZhP2sNO7OQ/services.webp",
                        "type": "PHOTO"
                    },
                    {
                        "url": "None",
                        "type": "PHOTO"
                    }
                ],
                "title": "Business Hours",
                "description": "Experience a full range of high-end, top-quality services using the best beauty products and styling."
            }
        },
        "contact_form": {
            "design": {
                "color": {
                    "border": "--color-text-P90",
                    "background": "--color-text-P100",
                    "input_text": "--color-text-P0",
                    "input_label": "--color-text-P0",
                    "btn_hover_bg": "--color-P30",
                    "input_border": "--color-text-P90",
                    "submit_cta_text": "--color-text-P100",
                    "description_text": "--color-text-P0",
                    "input_background": "--color-P110",
                    "customer_type_text": "--color-text-P10",
                    "after_submit_loader": "--color-text-P0",
                    "customer_type_border": "--color-text-P90",
                    "submit_cta_background": "--color-S50",
                    "customer_type_border_hover": "--color-P50",
                    "customer_type_selected_text": "--color-text-P100",
                    "customer_type_selected_border": "--color-P50",
                    "customer_type_selected_background": "--color-P50"
                }
            },
            "content": {
                "title": "Book Appointment",
                "description": "Book your appointment now by filling in the following details"
            }
        },
        "testimonials": {
            "design": {
                "color": {
                    "text": "--color-text-P10",
                    "date_text": "--color-text-P10",
                    "name_text": "--color-text-P0",
                    "card_border": "--color-text-P90",
                    "morelink_text": "--color-P50",
                    "card_background": "--color-text-P100",
                    "morelink_text_hover": "--color-P50"
                }
            },
            "content": {
                "title": "Testimonials",
                "description": "Discover the positive feedbacks from my valued clients"
            }
        }
    },
    "service_template": "service_template",
    "email": "twinn.touch.02@gmail.com",
    "data_version": 50,
    "color_scheme": {
        "primary": {
            "type": "color",
            "value": [
                332.92,
                85.15,
                44.9
            ],
            "valueType": "hsl"
        },
        "tertiary": {
            "type": "color",
            "value": [
                332.92,
                85.15,
                44.9
            ],
            "valueType": "hsl"
        },
        "secondary": {
            "type": "color",
            "value": [
                332.92,
                85.15,
                44.9
            ],
            "valueType": "hsl"
        },
        "textPrimary": {
            "type": "color",
            "value": [
                24,
                6,
                50
            ],
            "valueType": "hsl"
        },
        "textSecondary": {
            "type": "color",
            "value": [
                24,
                6,
                50
            ],
            "valueType": "hsl"
        }
    },
    "font_scheme": {
        "body_font": {
            "link": "https://fonts.googleapis.com/css2?family=Lato",
            "name": "Lato",
            "family": "sans-serif"
        },
        "head_font": {
            "link": "https://fonts.googleapis.com/css2?family=Quicksand",
            "name": "Quicksand",
            "family": "sans-serif"
        }
    },
    "sections": [
        {
            "id": 110,
            "name": "header",
            "type": "header"
        },
        {
            "id": 131,
            "name": "Home",
            "type": "banner"
        },
        {
            "id": 137,
            "name": "About Us",
            "type": "working_hrs"
        },
        {
            "id": "157",
            "name": "Services",
            "type": "category"
        },
        {
            "id": 116,
            "name": "Gallery",
            "type": "gallery"
        },
        {
            "id": 115,
            "name": "Testimonials",
            "type": "testimonials"
        },
        {
            "id": 138,
            "name": "Contact Us",
            "type": "contact_form"
        },
        {
            "id": 117,
            "name": "FAB",
            "type": "fab_mobile"
        },
        {
            "id": 133,
            "name": "footer",
            "type": "footer"
        }
    ],
    "path": "home",
    "base_template": "landing_page/master_v3",
    "location": "locations/11800823111557566790",
    "meta": {
        "description": "Twinn Touch fuses nail artistry and beauty care to cultivate a symphony of elegance. Here, personal style meets expert technique, transforming each appointment into an experience of indulgence. Step into a world where beauty meets sophistication at Twinn Touch."
    },
    "uid": "b5943ee7-2bc5-4302-87c9-71402eb30970",
    "variation": "A",
    "fb_pixel_id": "578041107831820"
}



# update_data_df = pd.read_csv("update_form_data.csv")

# def convert_to_dict(string):
#     return ast.literal_eval(string)

# update_data_df['form_data'] = update_data_df['form_data'].apply(convert_to_dict)
# update_data = json.loads(update_data_df.to_json(orient="records"))
# update_query = bulk_update_table("sp_website_form","id",update_data)

sql()
update_sql('gmb_website_details',update_data,"where id='512'")
conn.commit()

print(0)


