import requests
import json

id = "889f14ca-abc3-4cde-ab41-ea4411df470f"

url = f"https://api.clevertap.com/1/profile.json?identity={id}"

payload = {}
headers = {
  'X-CleverTap-Account-Id': '654-Z5R-946Z',
  'X-CleverTap-Passcode': '19bd7fcc423e4770a6dcd4265c073be2',
  'Content-Type': 'application/json'
}

# payload = json.dumps({
#   "deviceId": 
# })

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

