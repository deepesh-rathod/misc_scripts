import os
import json
import google.oauth2.credentials
import google_auth_oauthlib
import googleapiclient.discovery as gapd
from datetime import time, timedelta
import uuid
from requests import request
import re

ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "postgres"
REGION = "us-east-1c"
DBNAME = "postgres"
PASS = "March2021"
SECRET = "04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c"

import psycopg2
import pandas as pd
from datetime import datetime, date, timedelta


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


def update_sql(table, data, place_id):
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

    query += f" where place_id='{place_id}'"
    try:
        sql_query(query)
        conn.commit()
        return "Success"
    except Exception as e:
        return str(e)


# place_ids = ['ChIJp0LwEwcAK4cRbWjzyB04ccI']
# for place_id in place_ids:
#     website_services=[]
#     services_q = f"select * from user_services where place_id='{place_id}'"
#     sql_query(services_q)
#     res=cur.fetchall()

#     website_services_q = f"select services from gmb_website_details where place_id='{place_id}'"
#     sql_query(website_services_q)
#     services_res=cur.fetchall()
#     services=json.loads(services_res[0][0])
#     i=0
#     for cat in services:
#         w_services=[]
#         for r in res:
#             if r[2].replace("\n","")==cat['website category']:
#                 price=''
#                 if r[8]=='STARTS_FROM':
#                     price='$'+str(round(r[9]))+'+' if r[9] is not None else ''
#                 elif r[8]=='FIXED':
#                     price='$'+str(round(r[9])) if r[9] is not None else ''
#                 elif r[8]=='RANGE':
#                     price = '$'+str(round(r[9]))+'-'+'$'+str(round(r[6])) if r[9] is not None else ''
#                 elif r[8]=='NO_PRICE':
#                     price=''
#                 w_services.append({
#                     'name':r[1],
#                     'price':price,
#                     'description':r[3]
#                 })
#         cat['services']=w_services
#         i += 1
#     website_services = json.dumps(services)
#     website_services = website_services.replace("'", "''")

#     update_q = f"update gmb_website_details set services='{website_services}' where place_id='{place_id}-mt'"
#     sql_query(update_q)
#     conn.commit()


# place_id='ChIJp0LwEwcAK4cRbWjzyB04ccI'
# i=0

# website_Services_Q = f"select services from gmb_website_details where place_id='{place_id}'"
# sql_query(website_Services_Q)
# res=cur.fetchall()
# website_services_old = json.loads(res[0][0])

# services_q = f"select * from user_services where place_id='{place_id}'"
# sql_query(services_q)
# res=cur.fetchall()
# service_cats = []
# for r in res:
#     if r[2] not in service_cats:
#         service_cats.append(r[2])

# temp_website_services = []
# for cat in service_cats:
#     services_data = {
#         "category":cat,
#         "services":[]
#     }
#     for r in res:
#         if r[2]==cat:
#             price=''
#             if r[8]=='STARTS_FROM':
#                 price='$'+str(round(r[9]))+'+'
#             elif r[8]=='FIXED':
#                 price='$'+str(round(r[9]))
#             elif r[8]=='RANGE':
#                 price = '$'+str(round(r[9]))+'-'+'$'+str(round(r[6]))
#             elif r[8]=='NO_PRICE':
#                 price=''
#             services_data['services'].append({
#                 'name':r[1],
#                 'price':price,
#                 'description':r[3]
#             })
#     temp_website_services.append(services_data)
#     i += 1

# # old_cats = [data['website category'] for data in website_services_old]
# new_cats = [data['category'] for data in temp_website_services]


# for data in website_services_old:
#     for cat in temp_website_services:
#         if cat['category']==data['website category']:
#             data['services']=cat['services']

# website_services_old = [d for d in website_services_old if d.get('website category') in new_cats]


# ind = len(old_cats)
# for cat in new_cats:
#     if cat not in old_cats:
#         website_services_old.append({
#             'website category':cat,
#             "cat_img": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/cat_{ind+1}.webp",
#             "cat_desc": "Some random description which should be stored in category and description bank.",
#             "services": next(d['services'] for d in temp_website_services if d.get('category')==cat),
#         })
#         ind+=1


# website_services = json.dumps(website_services_old)
# website_services = website_services.replace("'", "''")
# update_q = f"update gmb_website_details set services='{website_services}' where place_id='ChIJp0LwEwcAK4cRbWjzyB04ccI-mt'"
# sql_query(update_q)
# conn.commit()

place_id = "ChIJp0LwEwcAK4cRbWjzyB04ccI"

# website_Services_Q = f"select * from user_services where place_id='{place_id}'"
# sql_query(website_Services_Q)
# res=cur.fetchall()

# cats = [r[2] for r in res]
# unique_cats = list(set(cats))

# new_webste_services = []
# ind = 0
# for cat in unique_cats:
#     services_data = {
#         "website category":cat,
#         "services":[],
#         "cat_img": f"https://d15e7bk5l2jbs8.cloudfront.net/{place_id}/cat_{ind+1}.webp",
#         "cat_desc": "Some random description which should be stored in category and description bank.",
#     }
#     for r in res:
#         if r[2]==cat:
#             price=''
#             if r[8]=='STARTS_FROM':
#                 price='$'+str(round(r[9]))+'+'
#             elif r[8]=='FIXED':
#                 price='$'+str(round(r[9]))
#             elif r[8]=='RANGE':
#                 price = '$'+str(round(r[9]))+'-'+'$'+str(round(r[6]))
#             elif r[8]=='NO_PRICE':
#                 price=''
#             services_data['services'].append({
#                 'name':r[1],
#                 'price':price,
#                 'description':r[3]
#             })
#     new_webste_services.append(services_data)
#     ind+=1

# website_services = json.dumps(new_webste_services)
# website_services = website_services.replace("'", "''")
# update_q = f"update gmb_website_details set services='{website_services}' where place_id='{place_id}-mt'"
# sql_query(update_q)
# conn.commit()
# print(0)

# website_status_query = f"select gws.status,god.biz_name,gws.url from gmb_website_status_new gws join gmb_retool_onboarding_details god on god.place_id=gws.place_id where gws.place_id='abdef123456abc123abcd1234b1'"
# sql_query(website_status_query)
# res = cur.fetchall()
# print(0)

old_data = {
    "url": "deepesh",
    "place_id": "abdef123456abc123abcd1234b1",
    "category": "Skin care clinic",
    "biz_name": "Deepesh Timely AI",
    "address": "1 Baywood Ave #3, San Mateo, CA 94402\n\n\n\n",
    "logo_link": "https://chrone-website.s3.us-east-2.amazonaws.com/ChIJL1wNMU-fj4ARzML8e5Pgdy4/logo.png",
    "working_hours": '[{"day": "MONDAY", "hours": "8 AM - 7 PM"}, {"day": "TUESDAY", "hours": "8 AM - 7 PM"}, {"day": "WEDNESDAY", "hours": "8 AM - 7 PM"}, {"day": "THURSDAY", "hours": "8 AM - 7 PM"}, {"day": "FRIDAY", "hours": "8 AM - 7 PM"}, {"day": "SATURDAY", "hours": "8 AM - 7 PM"}, {"day": "SUNDAY", "hours": "Closed"}]',
    "services_banner": "https://chrone-website.s3.us-east-2.amazonaws.com/ChIJL1wNMU-fj4ARzML8e5Pgdy4/services_banner.webp",
    "number": "(650) 762-5246",
    "biz_desc": "",
    "services": '[\n    {\n        "website category": "HydraFacial MD",\n        "cat_img": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/cat_0.webp",\n        "cat_desc": "Deep clean, exfoliate, extract, and hydrate your skin with our non-invasive multi-step facial for a refreshed and radiant complexion.",\n        "services": [\n            {\n                "name": "Express Hydrafacial",\n                "price": "$225",\n                "description": "An excellent choice for most skin types as this technology treats an array of skincare concerns ranging from congestion, tone and texture, fine lines and wrinkles and discoloration. HydraFacial uses a unique, patented Vortex-Fusion delivery system to exfoliate, extract and hydrate skin, and the spiral design delivers painless extractions. Consider a Luxe HydraFacial which incorporates an added speciality booster serum to target your specific skin concerns,"\n            },\n            {\n                "name": "Luxe Hydrafacial",\n                "price": "$250",\n                "description": "The invigorating treatment includes deeply cleansing, exfoliating, and extracting any impurities from the skin while simultaneously infusing nourishing ingredients for maximum hydration. The Luxe HydraFacial also includes a personalized Speciality Booster Serum  to address your specific skin concerns as well LED Light Therapy to further reduce visible signs of aging."\n            },\n            {\n                "name": "Clarifying HydraFacial",\n                "price": "$265",\n                "description": "Includes extended extractions, a personalized specialty booster serum,  high frequency to destroy acne causing bacteria, and LED light therapy for oily and congested skin.  Highly recommended for acne prone skin."\n            },\n            {\n                "name": "Platinum HydraFacial",\n                "price": "$295",\n                "description": "The ultimate HydraFacial experience! The detoxification process begins with Lymphatic Drainage which helps to remove toxins, slim and de-puff the face.  Followed by deeply cleansing, exfoliating, extracting and hydrating the skin while incorporating a Speciality Booster Serum that  targets your specific skin concern and LED Light Therapy to further reduce the visible signs of aging."\n            },\n            {\n                "name": "Pleased to Meet You HydraFacial",\n                "price": "$199",\n                "description": "You''re curious and we''d love to meet you. Enjoy your first HydraFacial at a special introductory price. Our introductory HydraFacial deeply cleanses, gently exfoliates and hydrates through serums filled with antioxidants, peptides and hyaluronic acids."\n            },\n            {\n                "name": "HydraFacial Hair - Keravive",\n                "price": "$495",\n                "description": "Using HydraFacial Vortex Technology and Keravive Peptide Complex Solution, this unique and relaxing treatment is designed to cleanse, stimulate, nourish, and hydrate your scalp for fuller and healthier hair.  Is a gentle 3-step process.  A 30-Day Scalp Health Spray is included to enhance the benefits of the in-office treatment and delivery daily nourishment between appointments. $495 per treatment and $1350 for a series of 3"\n            },\n            {\n                "name": "Dermaplaning Add-On to any HydraFacial",\n                "price": "$60",\n                "description": "When you pair Dermaplaning with HydraFacial you will see even more potent benefits.  Products penetrate deeper, fine lines are further reduced, and the skin glows even more."\n            },\n            {\n                "name": "HydraFacial Enhancement Neck",\n                "price": "$50",\n                "description": null\n            },\n            {\n                "name": "HydraFacial Enhancement Neck and Decollete",\n                "price": "$80",\n                "description": null\n            },\n            {\n                "name": "HydraFacial Perk Lip Treatment",\n                "price": "$30",\n                "description": "HydraFacial Lip Perk\\u2122 is a unique treatment that has been specially designed to treat the lip area and is both gentle and quick with immediate visible results. This treatment is fantastic at helping to improve the condition of your lips, while also improving the natural colour of the lip tissue. The Lip Perk solution contains hyaluronic acid, which provides amazing hydration, resulting in a plumping effect on the lips."\n            },\n            {\n                "name": "HydraFacial Perk Eye Treatment",\n                "price": "$30",\n                "description": "Add to any Hydrafacial-Perk\\u2122 uses a unique hybrid system with roller-flex technology to gently remove surface layer dead skin cells and impurities while delivering vital antioxidants. This quick service uses light suction and a multi-peptide blend to help gently brighten, tone, and firm the outer eye area while maintaining hydration. The treatment vial transforms into a take-home product to extend the benefits for up to 30 days."\n            },\n            {\n                "name": "3-Pack Express HydraFacial",\n                "price": "$595",\n                "description": null\n            }\n        ]\n    },\n    {\n        "website category": "Facials",\n        "cat_img": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/cat_1.webp",\n        "cat_desc": "Achieve a healthy and glowing complexion with our customized facials that cleanse, exfoliate, nourish, and hydrate your skin.",\n        "services": [\n            {\n                "name": "Signature Custom Facial",\n                "price": "$175",\n                "description": "This customized facial treatment includes deep cleansing, exfoliation, extractions, and a customized medical-grade treatment mask. The treatment is then completed with a light massage and application of specially selected serums, hydrators and SPF. Plus custom recommendations for at-home skincare regime."\n            },\n            {\n                "name": "Microcurrent Facial",\n                "price": "$200",\n                "description": "A microcurrent facial is like strength training for your skin. It is a relaxing treatment that stimulates the facial muscles underneath the skin, which will help to improve and lift the facial contour, tone the skin, and reduce wrinkles.  Microcurrent also improves hydration and oxygenation in the skin which results in brighter skin that glows."\n            },\n            {\n                "name": "Teen Facial",\n                "price": "$150",\n                "description": "This customized teen facial consists of a deep cleansing facial, softening and exfoliating the skin, and gentle extractions. A specifically targeted mask will calm the skin and fight future breakouts. Consultation and education on an at-home regime (18 and under)."\n            },\n            {\n                "name": "Glycolic Add on to Facial",\n                "price": "$50",\n                "description": "Add an additional Glycolic booster to your Custom Facial for deeper exfoliation targeting texture, acne, pores, and laxity."\n            },\n            {\n                "name": "Add on Neck and D\\u00e9collet\\u00e9 Treatment",\n                "price": "$65",\n                "description": "Add a Neck and D\\u00e9collet\\u00e9 Treatement to your Facial service"\n            }\n        ]\n    },\n    {\n        "website category": "Peels",\n        "cat_img": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/cat_2.webp",\n        "cat_desc": "Renew your skin and reduce signs of aging with our effective peels that exfoliate, stimulate collagen production, and improve skin texture and tone.",\n        "services": [\n            {\n                "name": "VI Peel",\n                "price": "$350",\n                "description": "VI Peel professional treatments feature a one-of-a-kind formulation designed to painlessly lift pigment, relieve acne and acne scars, and fight fine lines. See real results with VI Peel: the #1 Chemical Peel on the market today!"\n            },\n            {\n                "name": "Custom Chemical Peel",\n                "price": "",\n                "description": "This customized facial treatment includes deep cleansing, exfoliation, extractions, a customized medical-grade treatment mask and a corrective or restorative resurfacing chemical peel. The treatment is then completed with a light massage and application of specially selected serums, hydrators and SPF.\\n*3-4 week skin preparation required in most cases.\\n"\n            }\n        ]\n    },\n    {\n        "website category": "Microcurrent",\n        "cat_img": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/cat_3.webp",\n        "cat_desc": "Lift, tone, and sculpt your facial muscles with our painless microcurrent treatment that stimulates collagen production, reduces inflammation, and improves circulation.",\n        "services": [\n            {\n                "name": "Microcurrent Facial",\n                "price": "$200",\n                "description": "A microcurrent facial is like strength training for your skin. It is a relaxing treatment that stimulates the facial muscles underneath the skin, which will help to improve and lift the facial contour, tone the skin, and reduce wrinkles.  Microcurrent also improves hydration and oxygenation in the skin which results in brighter skin that glows."\n            },\n            {\n                "name": "Microcurrent 5 Pack",\n                "price": "$900",\n                "description": "Discounted pricing for pre-purchasing 5 sessions"\n            },\n            {\n                "name": "Microcurrent 10-pack",\n                "price": "$1700",\n                "description": "Discount for pre-purchasing 10 sessions"\n            },\n            {\n                "name": "Add Neck and D\\u00e9colletage to Microcurrent Facial",\n                "price": "$65",\n                "description": "Add the Neck and D\\u00e9colletage to your Microcurrent Facial"\n            }\n        ]\n    },\n    {\n        "website category": "Microneedling",\n        "cat_img": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/cat_4.webp",\n        "cat_desc": "Improve your skin’s appearance with SkinPen Microneedling which stimulates collagen and elastin production, improves facial scars, and reduces fine lines and wrinkles.",\n        "services": [\n            {\n                "name": "Microneedling Face",\n                "price": "$495",\n                "description": "SkinPen is the first FDA cleared Microneedling device.  It is clinically proven to improve the appearance of acne scars, hyperpigmentation, and fine lines and wrinkles.By creating tiny channels, or micro-injuries on your skin the micro-needling process stimulates your skin to repair itself, creating new collagen without any scar formation. At Sheila Marie Aesthetics we combine SkinPen technology with AnteAGE Growth Factor and Cytokine technology to further boost results."\n            },\n            {\n                "name": "Microneedling 3-Pack",\n                "price": "$1350",\n                "description": null\n            },\n            {\n                "name": "Microneedling Neck and D\\u00e9colletage",\n                "price": "$225",\n                "description": null\n            }\n        ]\n    },\n    {\n        "website category": "Body and Scalp",\n        "cat_img": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/cat_5.webp",\n        "cat_desc": "Our HydraFacial Keravive Scalp treatment will cleanse, exfoliate, and enhance the growth of thicker and fuller hair and our Back Treatments will improve texture, tone, remove impurities, and hydrate your skin.",\n        "services": [\n            {\n                "name": "The Custom Back Treatment",\n                "price": "$195",\n                "description": "This customized back treatment includes deep cleansing, exfoliation, extractions, and a customized treatment mask. The treatment is then completed with a massage and application of specially selected serums and hydrators."\n            },\n            {\n                "name": "HydraFacial Keravive Treatment",\n                "price": "$495",\n                "description": "This unique 3-step treatment cleanses, nourishes & hydrates the scalp for fuller, healthier hair. Addresses dry skin, clogged follicles & lack of circulation. Exfoliates while infusing a unique blend of growth factors providing nourishment and stimulation to the hair follicles."\n            },\n            {\n                "name": "HydraFacial Keravive 3 Session Series",\n                "price": "$1350",\n                "description": "Hydrafacial Keravive produces best results when done in a set of 3 treatments. Each treatment includes in office appointment + 30 day take home spray. This is ideal for thinning hair to get the best outcome."\n            },\n            {\n                "name": "HydraFacial Back Treatment",\n                "price": "$295",\n                "description": "HydraFacial Back treatment provides cleansing, exfoliation, extractions, and hydration, including Vortex-Fusion of antioxidants, peptides, and hyaluronic acid. This treatment includes a glycolic and salicylic acid peel."\n            }\n        ]\n    },\n    {\n        "website category": "Lashes and Brows",\n        "cat_img": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/cat_6.webp",\n        "cat_desc": "Enhance your natural beauty with our lash lifting, brow lamination, and tinting services that give the appearance of thicker and fuller lashes and brows.",\n        "services": [\n            {\n                "name": "Lash Lift with Tint",\n                "price": "$105",\n                "description": "Lash lifting opens the eyes, gives the appearance of longer, thicker, darker lashes and offers much less maintenance than eyelash extensions. Lifted lashes can last up to 8 weeks. Results are retained even after showering or swimming."\n            },\n            {\n                "name": "Lash Lift with Brow Lamination Combo",\n                "price": "$175",\n                "description": "Get that ultimate wow factor when you combine a lash lift, brow lamination, and tinting."\n            },\n            {\n                "name": "Lash or Brow Tint",\n                "price": "$45",\n                "description": "Tinting only "\n            },\n            {\n                "name": "Brow Lamination with Tint",\n                "price": "$95",\n                "description": "Brow lamination gives the appearace of fuller eyebrows that are more easily shaped into brows that you will love."\n            }\n        ]\n    },\n    {\n        "website category": "Add-Ons",\n        "cat_img": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/cat_7.webp",\n        "cat_desc": "Elevate your service with our add-on’s such as dermaplaning, hydro jelly masks, and LED light therapy to achieve your specific beauty goals.",\n        "services": [\n            {\n                "name": "Skin Care Consultation",\n                "price": "$0",\n                "description": "Complimentary 30 minute in depth skin care consultation to determine treatment plan.  "\n            },\n            {\n                "name": "LED Light Therapy",\n                "price": "$25",\n                "description": "Get LED light added to your Custom Facial or HydraFacial - 10 minutes.  Red light address aging and Blue light address acne."\n            },\n            {\n                "name": "Hydro Jelly Mask Add-on",\n                "price": "$30",\n                "description": "Hydro jelly masks are infused with electrolytes to boost skin hydration.  These masks form a vacuum-like seal that compress facial contours helping with overall circulation.  Formulated with refined algae, electrolytes and organic active ingredients.  "\n            },\n            {\n                "name": "Dermaplane Add-on",\n                "price": "$90",\n                "description": "Dermaplaning is a safe and highly effective physical exfoliation procedure.  Using a sterile, surgical scalpel to gently \\"shave\\" off the skins surface, gently removing the top most layer of dead skin.  The process triggers the cell regeneration process and allows products to better penetrate skin.  Also excellent at removing excess fine hairs which can often accumulate dirt and oil."\n            },\n            {\n                "name": "Extended Extractions",\n                "price": "$25",\n                "description": "For those who have more than just the T-zone area extractions. This add-on is good for those who have heavily congested pores and need more deep extractions."\n            },\n            {\n                "name": "Add Microcurrent to any Facial",\n                "price": "$75",\n                "description": "Get 20 minutes of Microcurrent added to your HydraFacial, Chemical Peel, or Custom Facial.  You will get instant lift utilizing the Pico Tone setting."\n            }\n        ]\n    }\n]',
    "testimonials": '[{"id": "AbFvOqlTtVSWBhNpmuLfu-JDv6cxfeCkGWcbC48WBEbgeP4tCb0ozSkwrziaIixTQWVzuRgJ2zMuqQ", "name": "Isis Contreras", "photo": "https://lh3.googleusercontent.com/a-/ACB-R5QTuri9axiDcNY131F1GYSm9_BFAXzfW4OK84pQ-A=s120-c-c0x00000000-cc-rp-mo-br100", "review": "I cant say enough great things, Sheila is a master at her profession.  I love the fact the I finally found a VI Peel provider that understands my skin type and tone, which is very important to women of color.  Ive had a microneedling and VI Peel treatments and Ive had fantastic support before and after treatment, Sheila has contacted me after each treatment to make sure I was doing ok, that is really unheard of now and days.  My skin is glowing and the sun damage is starting to fade, its amazing what two treatments can accomplish when you have the right provider.  I cant thank Sheila enough she is amazing!", "star": "FIVE", "date": "2022-12-26"}, {"id": "AbFvOqkEq9HJL6nM8LeflUTfl7YumSvhF-iUUg-eLshn2MvyPYSXZAen2drcNlg-Q9e46GvBwEPB", "name": "Tiffany Sutphen", "photo": "https://lh3.googleusercontent.com/a/AGNmyxbUoipY4hhpx95XRYRxGtvpsbKOWCDEbLodcsDO=s120-c-c0x00000000-cc-rp-mo-br100", "review": "Sheila provided me with a micro needling service. Her studio was very clean and she was very welcoming and professional. She explained to me the process since I never had it done before and continued to check in with me about my pain tolerance through the service. I was absolutely in love with this service with her that I couldn\\u2019t stop telling everyone about it. I definitely will be getting more micro needling in the future as my face looked the best it has ever looked after. My complexion was smooth, even toned and more firm. I would recommend anyone in the peninsula to go see her!!", "star": "FIVE", "date": "2023-01-03"}, {"id": "AbFvOqmbmmJ0C9rHwjIkOpyDePgMmGu67aI-uHMVzHE0xhh0uAdACAGRvPh0hFFsQyLy8DU2pJKgbw", "name": "Sue S i n g h", "photo": "https://lh3.googleusercontent.com/a/AGNmyxZrUwFdFG5irtR5WXpRDpWTJVNAk4gsYahqYkxT=s120-c-c0x00000000-cc-rp-mo-br100", "review": "I went in for a Hydrafacial with Sheila as I have developed melasma and was looking on how to get rid of it.\\nSheila was very professional.  She communicated and explained to me what she was going to do before starting and as she did them. I felt so relaxed and really enjoyed my Hydrafacial with her. My skin felt great after and I noticed that my melasma (dark spots) was lighter.  I loved it so much that I have been back 3 more times since than. Melasma has considerably lightened up.\\nGoing to try the Peel next.\\nThank You Sheila!", "star": "FIVE", "date": "2023-01-04"}, {"id": "AbFvOqkajC409jShV4oaEQWHKM3n1oeMVs-MiE9j8EYwIqn1jlqnYMgI-Ho80vVr6LXCBcZklfoQ", "name": "grace sim", "photo": "https://lh3.googleusercontent.com/a-/ACB-R5Rv3c-KeAJahRT6kcbLbIrPqpgje6IrqzGowPhzhQ=s120-c-c0x00000000-cc-rp-mo-br100", "review": "For 5 consecutive months, Ive been seeing Sheila for hydrafacials and have seen AMAZING changes to my skin. Before seeing Sheila, I had dry skin & uneven texture. With consecutive hydrafacials & Sheila\\u2019s product recommendations / expertise, my skin is GLOWING and smooth as can be. I get compliments on my skin all the time now! Everyone\\u2019s skin journey is different, but I highly recommend seeing a skin care expert (specifically Sheila) to guide and navigate you to resolve your skin concerns.", "star": "FIVE", "date": "2022-10-26"}, {"id": "AbFvOqmu5hk2hELZ0zE4ufBYdvdETPSBvvy8ScPb5yug3tTlDAR-Y0zTZvUATnt5YSzxPFTB-z18rg", "name": "Albert Silveira", "photo": "https://lh3.googleusercontent.com/a/AGNmyxbQS_zSUaiaJWOPYW7VDRQY7FvvovM5GTkBv_Ej=s120-c-c0x00000000-cc-rp-mo-br100", "review": "I treated my wife to her very first HydraFacial Kerative hair and scalpTreatment from Sheila Marie Aesthetics and she was very impressed. Sheilas studio is immaculate and the peaceful/relaxing background music made her feel very calm. \\u00a0As Sheila expertly performed the procedure, she patiently explained the reason for each step. \\u00a0My wife says that her hair feels thicker and she couldnt be happier. \\u00a0She will certainly do it again.", "star": "FIVE", "date": "2023-02-08"}, {"id": "AbFvOql-x2H9kZGtEuat9BYBBwdT9-gV52X8GtIf84eNTdAOMF2uWdaTWgEVhgieF4Snc2dbdxNS", "name": "Mecia Serafino", "photo": "https://lh3.googleusercontent.com/a-/ACB-R5RXHuIP9CkNwYnulbNuCPx4qtnsTJ4tEQ2cZoJr_04=s120-c-c0x00000000-cc-rp-mo-br100", "review": "Sheila did a wonderful job on my lashes and brows. Shes very professional and even through i have sensitive eyes and was tearing (my eyes water at the slightest provocation), she made them look beautiful. They lasted a good 3/4 weeks and I loved they way it turned out!  Id never had a brow lamination done and she made it look natural and effortless! I highly recommend Sheilas work. Looking forward to trying out her facials!", "star": "FIVE", "date": "2022-03-31"}]',
    "images": '[\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/1.jpg"\n    },\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/2.jpg"\n    },\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/3.jpg"\n    },\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/4.jpg"\n    },\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/5.png"\n    },\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/7.jpg"\n    },\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/8.jpg"\n    },\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/9.jpg"\n    },\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/10.jpg"\n    },\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/11.jpg"\n    },\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/12.jpg"\n    },\n    {\n        "type": "PHOTO",\n        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/13.jpg"\n    }\n]',
    "title": "Website title",
    "booking_link": "https://squareup.com/appointments/book/3wkzm2cniph47e/LDJ5ZESW6B7FQ/services",
    "index_template": "new_template_v7",
    "cat_img": "https://chrone-website.s3.us-east-2.amazonaws.com/ChIJL1wNMU-fj4ARzML8e5Pgdy4/services.webp",
    "banner": "https://chrone-website.s3.us-east-2.amazonaws.com/ChIJL1wNMU-fj4ARzML8e5Pgdy4/banner.webp",
    "hero_title": "Results Driven Skincare",
    "hero_desc": "Sheila Marie Aesthetics is a boutique skincare practice that provides personalized care to help you look and feel your best. From facials and peels to dermaplaning & microneedling, Sheila Marie has the expertise and technology to help you achieve your skincare goals.\n\n",
    "book_text": "Book appointment",
    "sms_number": '["(650) 762-5246"]',
    "banner_phn": "null",
    "submit_text": "Select Services",
    "section_data": {
        "about": {
            "media": [
                {
                    "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/about.webp",
                    "type": "photo",
                }
            ],
            "design": {},
            "content": {
                "about_text": "Sheila Marie discovered her passion for Aesthetics in 2015 when she was a sales representative for a leading medical grade skincare company. She learned all about the science of skincare and how specific ingredients,products, and treatments can target the skin from the inside out to produce real change. As a licensed Aesthetician, her philosophy is focused on customizing treatment plans specific to each client while utilizing best in class products and treatments. She believes everyone has the potential to uncover their best skin and is passionate about delivering real results. In her spare time Sheila Marie enjoys spending time with her daughter, surfing, practicing yoga, and staying educated and trained on what’s new in the world of Aesthetics.",
                "about_title": "About Sheila Marie",
            },
        },
        "banner": {
            "design": {},
            "content": {
                "media": [
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/banner.webp",
                        "type": "PHOTO",
                    },
                    {"url": "null", "type": "PHOTO"},
                ],
                "title": "Results Driven Skincare",
                "description": "Sheila Marie Aesthetics is a boutique skincare practice that provides personalized care to help you look and feel your best. From facials and peels to dermaplaning & microneedling, Sheila Marie has the expertise and technology to help you achieve your skincare goals.\n\n",
            },
        },
        "gallery": {
            "design": {},
            "content": {
                "media": [
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/1.jpg",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/2.jpg",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/3.jpg",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/4.jpg",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/5.png",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/7.jpg",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/8.jpg",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/9.jpg",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/10.jpg",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/11.jpg",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/12.jpg",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery/13.jpg",
                        "type": "PHOTO",
                    },
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/abdef123456abc123abcd1234b1/gallery/14.webp",
                        "type": "PHOTO",
                    },
                ],
                "title": "Gallery",
                "description": "Get a glimpse of our services with our inspiring gallery of images.",
            },
        },
        "category": {
            "design": {},
            "content": {
                "title": "Services",
                "description": "We offer a full range of the newest skincare technology and products.",
            },
        },
        "working_hrs": {
            "design": {},
            "content": {
                "media": [
                    {
                        "url": "https://d15e7bk5l2jbs8.cloudfront.net/ChIJL1wNMU-fj4ARzML8e5Pgdy4/services.webp",
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
                "title": "Make an Appointment",
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
    },
    "service_template": "service_template",
    "email": "sheilamarieskin@gmail.com",
    "data_version": 2,
    "color_scheme": {
        "primary": {"type": "color", "value": [198, 40, 61], "valueType": "hsl"},
        "tertiary": {"type": "color", "value": [198, 40, 61], "valueType": "hsl"},
        "secondary": {"type": "color", "value": [198, 40, 61], "valueType": "hsl"},
        "textPrimary": {"type": "color", "value": [24, 6, 50], "valueType": "hsl"},
    },
    "font_scheme": {
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
    },
    "sections": [
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
    ],
    "path": "services",
    "base_template": "landing_page/master_v2",
}
insert_sql("gmb_website_details", old_data)
