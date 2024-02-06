img_data = [
    {
        "website category": "Rice Milk Soap",
        "cat_img": "ChIJBeT232Hd2YgR2Ka0g6UNH6Y/temp/rice_milk_soap.jpg",
        "cat_desc": "$12",
    },
    {
        "website category": "Citrus Burst Soap",
        "cat_img": "ChIJBeT232Hd2YgR2Ka0g6UNH6Y/temp/citrus_burst_soap.jpg",
        "cat_desc": "$12",
    },
    {
        "website category": "Overnight Pimple Zapper",
        "cat_img": "ChIJBeT232Hd2YgR2Ka0g6UNH6Y/temp/overnight_pimple_zapper.jpg",
        "cat_desc": "$20",
    },
    {
        "website category": "Men's Beard Oil",
        "cat_img": "ChIJBeT232Hd2YgR2Ka0g6UNH6Y/temp/mens_beard_oil.jpg",
        "cat_desc": "$20",
    },
    {
        "website category": "Vitamin C Serum",
        "cat_img": "ChIJBeT232Hd2YgR2Ka0g6UNH6Y/temp/vitamin_c.jpg",
        "cat_desc": "$25",
    },
    {
        "website category": "Holy Yoni Oil",
        "cat_img": "ChIJBeT232Hd2YgR2Ka0g6UNH6Y/temp/holy_yoni_oil.jpg",
        "cat_desc": "$20",
    },
    {
        "website category": "Bath Salts",
        "cat_img": "ChIJBeT232Hd2YgR2Ka0g6UNH6Y/temp/bath_salt.jpg",
        "cat_desc": "$12",
    },
]

import requests
import json

url = "https://chroneinternal.com/api/update-photos"

for img in img_data:
    payload = json.dumps(
        {
            "bucket_name": "chrone-sp-website",
            "file_name": img["cat_img"]
            .replace("/temp", "")
            .replace(".jpg", "_new.webp"),
            "file_url": f"https://chrone-sp-website.s3.amazonaws.com/{img['cat_img']}",
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
