import requests
import json

url = "http://localhost:8080/api/create-sp-website"
website_creation_data = [
    {
        "place_id":"ChIJR0zvU-CdLIcR7QfxNNt7Js4",
        "data":{
            "url":"radiant-beauty-suites",
            "theme":"dark",
            "template":"braids"
        }
    }
]
for website_input_data in website_creation_data:
    res = requests.post(url , data= json.dumps(website_input_data['data']), params={'place_id':website_input_data['place_id']})
