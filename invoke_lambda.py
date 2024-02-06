import boto3
import json

lambda_client = boto3.client(
    'lambda',
    region_name='us-east-1'  # Replace with your desired AWS region
)

function_name = 'store_scrape_services'

services = [{
            "category": "",
            "name": "Policy cut “regular haircut”",
            "currency": "USD",
            "pricing_type": "FIXED",
            "price_start": 40.0,
            "price_end": 40.0,
            "description": "This consist of a blend on the side with a minimum amount of hair from a 1/2 Gaurd and higher. This is not a BALD FADE!!!",
            "duration": "35",
            "uid": "fb195d70-a296-4240-9bc1-4baaa90ca62a"
        },
        {
            "category": "",
            "name": "Original Cut And Shave",
            "currency": "USD",
            "pricing_type": "FIXED",
            "price_start": 50.0,
            "price_end": 50.0,
            "description": "This service consists of a Men's Haircut exfoliating facial with a massage to knock off all that nastiest you’ve acquired sense your last vist to give you want you need back in your life. Some Repect on ya Game.",
            "duration": "45",
            "uid": "fb195d70-a296-4240-9bc1-4baaa90ca62a"
        },
        {
            "category": "",
            "name": "Bald fade",
            "currency": "USD",
            "pricing_type": "FIXED",
            "price_start": 45.0,
            "price_end": 45.0,
            "description": "This service consists of Razor Fade on the sides  and a trim on top using shears or clippers.",
            "duration": "45",
            "uid": "fb195d70-a296-4240-9bc1-4baaa90ca62a"
        },
        {
            "category": "",
            "name": "The Royal Flush",
            "currency": "USD",
            "pricing_type": "FIXED",
            "price_start": 65.0,
            "price_end": 65.0,
            "description": "The \"Royal Flush\" is for any man with a Beard who is looking to go from a mess to the best looking version of himself. This include Haircut/ shave/ facial & Beard shaping(trimming).",
            "duration": "60",
            "uid": "fb195d70-a296-4240-9bc1-4baaa90ca62a"
        },
        {
            "category": "",
            "name": "\"The Triple Threat\" Cut/Shave/Eyebrow",
            "currency": "USD",
            "pricing_type": "FIXED",
            "price_start": 60.0,
            "price_end": 60.0,
            "description": "This service is put together for the guy who stays Fresh! Haircut, Shave, and eyebrow shaping with razor.",
            "duration": "45",
            "uid": "fb195d70-a296-4240-9bc1-4baaa90ca62a"
        },
        {
            "category": "",
            "name": "Women's cut & design w/clippers",
            "currency": "USD",
            "pricing_type": "FIXED",
            "price_start": 40.0,
            "price_end": 40.0,
            "description": "This service consists of a Woman’s haircut using the clippers. Designs are done upon request and may have additional charges.",
            "duration": "45",
            "uid": "fb195d70-a296-4240-9bc1-4baaa90ca62a"
        },
        {
            "category": "",
            "name": "“Kids Haircut”",
            "currency": "USD",
            "pricing_type": "FIXED",
            "price_start": 40.0,
            "price_end": 40.0,
            "description": "This service is for Kids 11 years old and younger.",
            "duration": "35",
            "uid": "fb195d70-a296-4240-9bc1-4baaa90ca62a"
        },
        {
            "category": "",
            "name": "Beard service",
            "currency": "USD",
            "pricing_type": "FIXED",
            "price_start": 30.0,
            "price_end": 30.0,
            "description": "This service is a hot towel applied with massager on hand. Giving you a relaxing vibe to ease the mind.  Then there will be an exfoliating cream to cleanse the top layer of skin peeping it for a shave on a clean surface reducing the risk of impurities  invading your face ending up with that pimp the always gets popped. No bueno.",
            "duration": "25",
            "uid": "fb195d70-a296-4240-9bc1-4baaa90ca62a"
        },
        {
            "category": "",
            "name": "Shape up",
            "currency": "USD",
            "pricing_type": "FIXED",
            "price_start": 25.0,
            "price_end": 25.0,
            "description": "",
            "duration": "25",
            "uid": "fb195d70-a296-4240-9bc1-4baaa90ca62a"
        }
    ]

# handler({"uid":"fb195d70-a296-4240-9bc1-4baaa90ca62a","scrapped_services": services},None)

payload = {"body" : {
    "uid":"fb195d70-a296-4240-9bc1-4baaa90ca62a",
    "scrapped_services":json.dumps(services),
    "from_website":False
}}


response = lambda_client.invoke(
    FunctionName=function_name,
    InvocationType='Event',  # Use 'Event' for asynchronous invocation
    Payload=json.dumps(payload)
)

response_payload = response['Payload'].read().decode('utf-8')
print(response_payload)