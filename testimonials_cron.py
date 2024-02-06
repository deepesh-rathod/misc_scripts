import psycopg2
import pandas as pd
import json
from datetime import datetime, date, timedelta
import requests

# ENDPOINT = "db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
# PORT = "5432"
# USR = "postgres"
# REGION = "us-east-1c"
# DBNAME = "postgres"
# PASS = "March2021"
# SECRET = "04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c"

# def sql():
#     global conn, cur
#     try:
#         conn = psycopg2.connect(
#             host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS
#         )
#         cur = conn.cursor()
#     except Exception as e:
#         print("ERROR", e)


# def sql_query(query):
#     global cur
#     try:
#         cur.execute(query)
#     except:
#         sql()
#         cur.execute(query)


# website_data_query = "select place_id,biz_name,sections,base_template from gmb_website_details where index_template ilike '%new%' and place_id='ChIJEaA4A5rFQIYR4eVQ_XgmZGU'"
# sql_query(website_data_query)
# website_data_res = cur.fetchall()

# try:
#     for data in website_data_res:
#         place_id = data[0]
#         biz_name = data[1]
#         sections = data[2]
#         base_template = data[3]

#         reviews_data_query = f"select * from review_data where place_id='{place_id}' and rating='5' and comment is not null order by date desc"
#         sql_query(reviews_data_query)
#         reviews_data = cur.fetchall()
#         website_reviews_data = []
#         for review_data in reviews_data[0:6]:
#             review_dict = {
#                 "id": review_data[0],
#                 "name": review_data[7],
#                 "photo": review_data[8],
#                 "review": review_data[1],
#                 "star": "FIVE",
#                 "date": review_data[6].strftime("%a, %d %b, %Y"),
#             }
#             website_reviews_data.append(review_dict)

#         testimonials_section_present = True
#         if len(website_reviews_data) != 0:
#             if "testimonials" not in str(sections):
#                 testimonials_section_present = False
#                 if "dark" in base_template:
#                     testimonials_section = {
#                         "id": "135",
#                         "name": "Testimonials",
#                         "type": "testimonials",
#                     }
#                     contact_form_index = next((index for (index, s) in enumerate(sections) if s["type"] == "contact_form"), None)
#                     sections.insert(contact_form_index,testimonials_section)
#                 else:
#                     testimonials_section = {
#                         "id": "115",
#                         "name": "Testimonials",
#                         "type": "testimonials",
#                     }
#                     contact_form_index = next((index for (index, s) in enumerate(sections) if s["type"] == "contact_form"), None)
#                     sections.insert(contact_form_index,testimonials_section)

#             if not testimonials_section_present:
#                 website_details_update_data = {
#                     "sections":sections,
#                     "testimonilas":json.dumps(website_reviews_data)
#                 }
#                 slack_notif_msg = f"Testimonials updated\nTestimonials section added\nBiz Name : {biz_name}"
#             else:
#                 slack_notif_msg = f"Testimonials updated\nBiz Name : {biz_name}"
#                 website_details_update_data = {
#                     "testimonilas":json.dumps(website_reviews_data)
#                 }
#             # update sql
#             # slack msg
# except Exception as e:
#     slack_notif_msg = f"Testimonials update error\nBiz Name : {website_data_res[0][1]}"
#     # slack error msg


resp = requests.get("https://detoxing-the-sole.chrone.work/")
print(0)
