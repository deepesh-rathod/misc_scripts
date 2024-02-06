import requests
import json

datas = [
  {
    "form_data": {
      "name": "Andrea Orozco",
      "phone": "4802805126",
      "service": "Not Selected",
      "message": "No message",
      "email": "Not given",
      "subscribe_text_message": "Yes"
    },
    "repeat_customer": "Returning Client",
    "selected_service": "Body Contouring - 1 session",
    "url": "https://north-central-massage.chrone.work",
    "initial_referrer": "www.google.com",
    "place_id": "ChIJAXNCoyRtK4cRw8hnTFQw0qc",
    "uid": "6176ea35-8222-45cc-9076-986f2f7d4aba",
    "utm_source": None
  },
  {
    "form_data": {
      "name": "Richa Shukla",
      "phone": "2408106485",
      "service": "Not Selected",
      "message": "No message",
      "email": "Not given",
      "subscribe_text_message": "Yes"
    },
    "repeat_customer": "New Client",
    "selected_service": "Shahnaz Regular",
    "url": "https://spa-elegant.chrone.work",
    "initial_referrer": "$direct",
    "place_id": "ChIJcX4BWyZFtokRQGUQTYGDQkE",
    "uid": "cedf3d37-d044-4f43-a40e-a084a814b21b",
    "utm_source": None
  },
  {
    "form_data": {
      "name": "Trenton hawley",
      "phone": "4805695551",
      "service": "Not Selected",
      "message": "No message",
      "email": "Not given",
      "subscribe_text_message": "Yes"
    },
    "repeat_customer": "New Client",
    "selected_service": None,
    "url": "https://slaybyvashae-bundles-and-braids.chrone.work",
    "initial_referrer": "www.google.com",
    "place_id": "ChIJvS10NXc_K4cRXltMSC0ADSw",
    "uid": "b886d0cc-dec4-444f-b877-1cae1ef06760",
    "utm_source": "googlemaps"
  },
  {
    "form_data": {
      "name": "Richa Shukla",
      "phone": "2408106485",
      "service": "Not Selected",
      "message": "No message",
      "email": "Not given",
      "subscribe_text_message": "Yes"
    },
    "repeat_customer": "New Client",
    "selected_service": None,
    "url": "https://spa-elegant.chrone.work",
    "place_id": "ChIJcX4BWyZFtokRQGUQTYGDQkE",
    "uid": "cedf3d37-d044-4f43-a40e-a084a814b21b",
    "utm_source": "googlemaps"
  },
  {
    "form_data": {
      "name": "Samuel Clark",
      "phone": "4695608669",
      "service": "Not Selected",
      "message": "No message",
      "email": "Not given",
      "subscribe_text_message": "Yes"
    },
    "repeat_customer": "New Client",
    "selected_service": None,
    "url": "https://shecosmosalon.chrone.work",
    "initial_referrer": "www.google.com",
    "place_id": "ChIJn8TRv2UYTIYR8lHIGHfUeoI",
    "uid": "309d5134-5ef5-4f15-9309-6712c83549f1",
    "utm_source": "googlemaps"
  },
  {
    "form_data": {
      "name": "Priscilla",
      "phone": "9093255236",
      "service": "Not Selected",
      "message": "No message",
      "email": "Not given",
      "subscribe_text_message": "Yes"
    },
    "repeat_customer": "New Client",
    "selected_service": None,
    "url": "https://lashed-by-jazz.chrone.work",
    "initial_referrer": "www.google.com",
    "place_id": "ChIJ8c1QzTm33IAR-eOSn5z98vY",
    "uid": "bc311a93-5fd5-45a2-981b-6158a583a3de",
    "utm_source": "googlemaps"
  },
  {
    "form_data": {
      "name": "Vanette",
      "phone": "4044383574",
      "service": "Not Selected",
      "message": "No message",
      "email": "Not given",
      "subscribe_text_message": "Yes"
    },
    "repeat_customer": "Returning Client",
    "selected_service": None,
    "url": "https://navi-k-salon.chrone.work",
    "initial_referrer": "l.instagram.com",
    "place_id": "ChIJMVE51g0F9YgRAHZtFdix6eo",
    "uid": "de3048df-1cdd-4908-8bc5-7baecb2a87af",
    "utm_source": "googlemaps"
  }
]

url = "http://localhost:8080/send-lead-sms-landingpage"

for d in datas:

    payload = json.dumps(d)

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)


