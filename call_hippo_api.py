import requests
import json

url = "https://web.callhippo.com/v1/sms/send"

payload = json.dumps({
  "from": "+18145594564",
  "to": "+18485653917",
  "userEmail": "kritwish@timelyai.com",
  "smsBody": "Test message from call hippo"
})
headers = {
  'apiToken': '64b03b912980381596ee26f4',
  'Content-Type': 'application/json',
  'User-Agent':'PostmanRuntime/7.35.0'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
