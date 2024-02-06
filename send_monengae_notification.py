import json
import requests

MOENGAGE_APP_ID = "PON39R5RUH5DYDQ4Q2239UIZ"
MOENGAGE_AUTH_BASE = (
    "UE9OMzlSNVJVSDVEWURRNFEyMjM5VUlaOmhkSFc2c3hpam5JU3dqOGxkZmNhNGNkRA=="
)

url = f"https://api-01.moengage.com/v1/event/{MOENGAGE_APP_ID}"

payload = json.dumps(
    {
        "type": "event",
        "customer_id": "1fc1c04f-8ab6-4bb0-abe1-6c5938df94e4",
        "actions": [
            {"action": "Campaign Pending Approval", "attributes": {"app_form_id": 153}}
        ],
    }
)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {MOENGAGE_AUTH_BASE}",
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response)
