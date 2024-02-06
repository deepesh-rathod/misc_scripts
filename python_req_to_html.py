import requests

url = "http://localhost:8080/campaign/flyer-templates?uid=fb195d70-a296-4240-9bc1-4baaa90ca62a&campaign_id=64"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

data = response.json()

for d in data["data"]:
    html_string = d["html"].replace("\n    ", "").replace('"', '"')

print(response.text)
