import requests
import json

url = "https://chroneinternal.com/api/update-photos"

for i in range(14):
    payload = json.dumps({
    "bucket_name": "chrone-sp-website",
    "file_name": f"ChIJ5SnxwZazt4kRGusZ74-QiXg/gallery/{i}_new.webp",
    "file_url": f"https://chrone-sp-website.s3.amazonaws.com/ChIJ5SnxwZazt4kRGusZ74-QiXg/temp/gallery/{i}_new.jpeg"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.status_code)
