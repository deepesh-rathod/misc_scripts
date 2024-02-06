ENDPOINT="db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="us-east-1c"
DBNAME="postgres"
PASS = "March2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

import requests
import json
import openai
import psycopg2
from psycopg2.extras import RealDictCursor

def sql():
    global conn, cur
    try:
        conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS)
        cur = conn.cursor(cursor_factory=RealDictCursor)
    except Exception as e:
        print("ERROR",e)

def sql_query(query):
    global cur
    try:
        cur.execute(query)
    except:
        sql()
        cur.execute(query)
    conn.commit()


def get_profile_data(uid):
    sql()
    profile_data_q = f"select * from gmb_retool_onboarding_details where uid='{uid}'"
    sql_query(profile_data_q)
    result = cur.fetchall()
    return dict(result[0]) if len(result)>0 else {}


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

OPENAI_ORG_ID = 'org-yM6MbuKD6qh8UR63H72ljeG1' #get_secret_value('OPENAI_ORG_ID')
OPENAI_API_KEY = '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' #get_secret_value('OPENAI_API_KEY')

openai.organization = OPENAI_ORG_ID
openai.api_key = OPENAI_API_KEY

def get_chat_gpt_answer(messages):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )
    return completion.choices[0]['message']['content'] # type: ignore

def get_categories_description(services,categories):
    message = f"""following is a list of beauty services of my business: "{str(services)}". Which are categorised into following categories {str(categories)}. Give me a short service desc for each category. Make it singular and generic. Make it 1 liner, and something simple. I want to eliminate our/we/my/I. Don't include {{}} in the ouput. Eg:- "Experience the ultimate smoothness with an exceptional service. Feel confident and carefree in your own skin.  Don't correct any spellings in the final result. Use the original spellings. Return the output in the form of json. {{category name: description}}"""
    messages = [
        {"role": "user", "content": message}
    ]
    try:
        print(messages)
        ans = get_chat_gpt_answer(messages)
        ans_json = json.loads(ans[:ans.index('}')+1])
    except:
        # logger.error()
        return {}
        raise
    return ans_json

def get_letters(input_string):
    return ''.join([char for char in input_string if char.isalpha()]).lower()

def insert_categories(categories,uid):
    formatted_categories = []
    for cat,desc in categories.items():
        formatted_category = {
            "name":cat,
            "description":desc,
            "photo":f"https://d15e7bk5l2jbs8.cloudfront.net/{uid}/{get_letters(cat)}.webp",
            "business_id":uid,
        }
        formatted_categories.append(formatted_category)
    
    # insert categories in DB
    sql()
    inserted_data = bulk_insert_sql("website_dev.categories",formatted_categories,conn)
    categories_in_db = []
    for data in inserted_data:
        categories_in_db.append(dict(data))
    return categories_in_db

def insert_services(services,categories,uid):
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
            "category_id": categories_with_id[service.get("category","").strip()],
        }
        formatted_services.append(formatted_service)

    # insert services in DB
    sql()
    inserted_data = bulk_insert_sql("website_dev.services",formatted_services,conn)
    services_in_db = []
    for data in inserted_data:
        services_in_db.append(dict(data))
    return services_in_db

def format_duration(duration):
    if duration=='' or duration is None or duration == 'null' or duration == 'NULL' or duration == 'Null':
        return None
    else:
        return int(float(duration))
    
def format_price(price):
    if price=='' or price is None or price == 'null' or price == 'NULL' or price == 'Null':
        return None
    else:
        return float(price)

def insert_service_variation(services,formatted_services):
    services_with_id = {}
    for service in formatted_services:
        services_with_id[service["name"] + service['category']] = service["id"]

    formatted_service_variations = []
    for variants in services:
        service_variant = {
            "service_id": services_with_id[variants.get("name") + variants.get("category")],
            "name": variants.get("name"),
            "duration": format_duration(variants.get("duration")),
            "price": format_price(variants.get("price_start")),
            "pricing_type":variants.get("pricing_type"),
            "description": variants.get("description")
        }
        formatted_service_variations.append(service_variant)

    # insert services in DB
    sql()
    inserted_data = bulk_insert_sql("website_dev.service_variations",formatted_service_variations,conn)
    services_variations_in_db = []
    for data in inserted_data:
        services_variations_in_db.append(dict(data))
    return services_variations_in_db
    

def get_new_services(services,categories,uid):
    formatted_categories = insert_categories(categories,uid)
    formatted_services = insert_services(services,formatted_categories,uid)
    formatted_service_variations = insert_service_variation(services,formatted_services)

    return formatted_categories,formatted_services,formatted_service_variations

def get_user_services_data(services,service_variations,profile_data):
    user_services = []

    for service in services:
        service_variation = next((sv for sv in service_variations if sv.get('service_id') == service['id']), {})
        user_service = {
          "place_id": profile_data['place_id'],
          "name": service['name'],
          "category": service['category'],
          "description": service['description'],
          "star": None,
          "service_id": service['id'],
          "price_end": service_variation.get('price'),
          "currency": None,
          "pricing_type": service_variation.get('pricing_type'),
          "price_start": service_variation.get('price'),
          "created_at": str(service['created_at']),
          "duration": service_variation.get('duration'),
          "location_id": profile_data['location'],
          "uid": profile_data['uid']
        }
    
        user_services.append(user_service)
    return user_services
    
booking_link = "https://squareup.com/appointments/book/jmax18mx54h12k/LRM18WSEEZXTT/start"
uid = "fb195d70-a296-4240-9bc1-4baaa90ca62a"

services = [
  {
    "name": "Hydration-Facial",
    "description": "Using the HydraFacial machines patented technology to cleanse, extract, and hydrate the skin.  Super serums are made with nourishing ingredients that create an instantly gratifying glow in just 3 steps. Add on LED LightStim therapy or Wet-Dermabrasion to address multiple skin issues including acne.",
    "price_start": 125,
    "price_end": 125,
    "pricing_type": "FIXED",
    "category": "Facial Treatment",
    "duration": "60.0",
    "uid": ""
  },
  {
    "name": "Chemical Peel Facial level 1",
    "description": "C-Vitality peel, Cascade Retinol Peel, Intensive brightening peel, or Mandelic Acid 35% AHA peel all are layered with a 30% Pumpkin Enzyme. This treatment address: texture, dull skin, inflammation, and as a pre-conditioning peel for more invasive peels. You will notice IMMEDIATE changes in the skin with famous AHA peels you can layer and customize!",
    "price_start": 125,
    "price_end": 125,
    "pricing_type": "FIXED",
    "category": "Facial Treatment",
    "duration": "60.0",
    "uid": ""
  },
  {
    "name": "Derma-Plane Facial",
    "description": "Derma-planning begins to unclog pores by gently removing dead skin cells and other impurities from your skin's surface. Targeted serums will be able to penetrate better and more evenly giving you the ultimate healthy-skin glow! Also removes vellus hair (peach fuss) for smoother make up application. These hairs DO NOT grow back darker or thicker.",
    "price_start": 125,
    "price_end": 125,
    "pricing_type": "FIXED",
    "category": "Facial Treatment",
    "duration": "60.0",
    "uid": ""
  },
  {
    "name": "Lymphatic Drainage Back Facial",
    "description": "Cleanse, exfoliate, extractions, mask and steam to remove dead skin cells, oils, and blackheads.  Massage and lymphatic drainage using the Hydra-Facials lymphatic back modality.",
    "price_start": 125,
    "price_end": 125,
    "pricing_type": "FIXED",
    "category": "Body Treatment",
    "duration": "90.0",
    "uid": ""
  },
  {
    "name": "Brow Tinting",
    "description": "Brow Tinting is a great way to color your brows. Sometimes there are small light hairs that can be colored to achieve fuller brows or to cover gray hairs.  Add-on brow shaping done with wax and or tweezing. Add-on Lamination for extra Beautiful Brows that last 4-6 weeks for tinting and 6-8 weeks for Lamination.",
    "price_start": 25,
    "price_end": 25,
    "pricing_type": "FIXED",
    "category": "Brows",
    "duration": "30.0",
    "uid": ""
  },
  {
    "name": "Brow Shaping/Wax",
    "description": "Brow shaping done with wax and or tweezing. Add-on Lamination and Tinting for extra Beautiful Brows that last 4-6 weeks for tinting and 6-8 weeks for Lamination.",
    "price_start": 25,
    "price_end": 25,
    "pricing_type": "FIXED",
    "category": "Brows",
    "duration": "5.0",
    "uid": ""
  },
  {
    "name": "Add-On Oxygen Infusion",
    "description": "Hydrating serums infused into the skin through an O2 infuser",
    "price_start": 25,
    "price_end": 25,
    "pricing_type": "FIXED",
    "category": "Add-on Treatment",
    "duration": "30.0",
    "uid": ""
  },
  {
    "name": "Add-on LightStim",
    "description": "Add-on to any facial, treatment, LED  LightStim is a patented technology that omits all the LED lights at once to treat multiple skin issues.",
    "price_start": 25,
    "price_end": 25,
    "pricing_type": "FIXED",
    "category": "Add-on Treatment",
    "duration": "30.0",
    "uid": ""
  },
  {
    "name": "New Client Skin Consultation with 1st Treatment",
    "description": "New Client Skin Consultation with 1st treatment same day.  1st time clients only.",
    "price_start": 89,
    "price_end": 89,
    "pricing_type": "FIXED",
    "category": "Facial Treatment",
    "duration": "90.0",
    "uid": ""
  },
  {
    "name": "Add-on Neck and décolleté",
    "description": "Add-on your Neck and Décolleté to any facial treatment.   Its an amazing add-on to My Level 1 Chemical Peel Facial.",
    "price_start": 25,
    "price_end": 25,
    "pricing_type": "FIXED",
    "category": "Add-on Treatment",
    "duration": "30.0",
    "uid": ""
  },
  {
    "name": "Organic In-Studio Teeth Whitening",
    "description": "Relax while getting your teeth whitened! We make it a pleasant and relaxing experience.  Sunna-Smile is organic and perfect for sensitive teeth.  Blue LED light is used to activate the organic beach and red LED light reduces sensitive.",
    "price_start": 149,
    "price_end": 149,
    "pricing_type": "FIXED",
    "category": "SunnaSmile ",
    "duration": "90.0",
    "uid": ""
  },
  {
    "name": "Follow-up In-Studio Teeth Whitening",
    "description": "In-House touch-up 1-6 weeks after initial whitening treatment when you bring back your beach pen.",
    "price_start": 75,
    "price_end": 75,
    "pricing_type": "FIXED",
    "category": "SunnaSmile ",
    "duration": "60.0",
    "uid": ""
  },
  {
    "name": "TCA or Jessner Chemical Peel",
    "description": "Level three chemical peels achieve amazing results with Dermodality.  The skin must be pre-conditioned 1st with level one peels and homecare products, length of time dependent on Fitzpatrick skin type.",
    "price_start": 249,
    "price_end": 249,
    "pricing_type": "FIXED",
    "category": "Facial Treatment",
    "duration": "90.0",
    "uid": ""
  },
  {
    "name": "Nano-Needling Facial",
    "description": "Nano-needling works by enhancing the skin's ability to absorb serums that are beneficial for the skin.  It also triggers the skins natural regenerative processes by boosting collagen and elastin production, which allows the skin to heal and address different target issues.",
    "price_start": 150,
    "price_end": 150,
    "pricing_type": "FIXED",
    "category": "Facial Treatment",
    "duration": "90.0",
    "uid": ""
  },
  {
    "name": "Add-On Nano Needling to Derma-Plane",
    "description": "Add-On to Nano-needling to your Derma-Plane Facial for an even deeper effective result.  Nano-Needling works by enhancing the skin's ability to absorb serums that are beneficial for the skin.  It also triggers the skins natural regenerative processes by boosting collagen and elastin production, which allows the skin to heal and address different target issues.",
    "price_start": 100,
    "price_end": 100,
    "pricing_type": "FIXED",
    "category": "Add-on Treatment",
    "duration": "30.0",
    "uid": ""
  },
  {
    "name": "Add-on Gua Sha",
    "description": "Facial Gua Sha is a technique used in traditional Chinese medicine that involves using stones and slowly stroking and massaging the face and neck to improve circulation and release tension, which leave it less puffy and more glowy.”",
    "price_start": 25,
    "price_end": 25,
    "pricing_type": "FIXED",
    "category": "Add-on Treatment",
    "duration": "30.0",
    "uid": ""
  },
  {
    "name": "Wet-dermabrasion",
    "description": "",
    "price_start": 25,
    "price_end": 25,
    "pricing_type": "FIXED",
    "category": "Add-on Treatment",
    "duration": "30.0",
    "uid": ""
  },
  {
    "name": "Brow Lamination",
    "description": "Brow lamination is a process of perming your brows hairs, but instead of curls, you get straighter, upward-facing hairs that are set in place.  Lasts 4-8 weeks.  Our Keratin innovative formula is specifically designed to combat lifted cuticles and seal down damaged hair cuticles, preventing future damage to your precious lashes and brows. Say goodbye to brittle, lackluster lashes/brows and hello to a glossy, shiny, and vibrant transformation",
    "price_start": 75,
    "price_end": 75,
    "pricing_type": "FIXED",
    "category": "Brows",
    "duration": "60.0",
    "uid": ""
  },
  {
    "name": "Lash Lift with Tint",
    "description": "Lash Lift Keratin is a process of perming your lash hairs to achieve curled upward-facing lashes that are set in place. Lasts 6-8 weeks. Our Keratin innovative formula is specifically designed to combat lifted cuticles and seal down damaged hair cuticles, preventing future damage to your precious lashes and brows. Say goodbye to brittle, lackluster lashes/brows and hello to a glossy, shiny, and vibrant transformation lasts 6-8 weeks. Tint is included in this price.",
    "price_start": 150,
    "price_end": 150,
    "pricing_type": "FIXED",
    "category": "Lashes",
    "duration": "120.0",
    "uid": ""
  }
]

categories = list(set([c['category'] for c in services]))

category_descriptions = get_categories_description(services,categories)

categories,services,service_variations = get_new_services(services,category_descriptions,uid)

profile_data = get_profile_data(uid)

user_services = get_user_services_data(services,service_variations,profile_data)

print(0)
