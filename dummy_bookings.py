import requests
import json
import random


min_value = 1
max_value = 100

# Generate a random number within the specified range
random_number = random.randint(min_value, max_value)

# Print the random number
print(random_number)

url = "http://chrone-dev-node-env.eba-t5g6xad2.us-east-1.elasticbeanstalk.com/schedule/bookings/create-booking"

month="10"
day="0"
start_hours="20"
end_hours="19"

status = ["BOOKED","UNAPPROVED"]
initiator = ["SP","EC"]

i=0
while i<1000:
    i+=1
    start_hours = random.randint(9, 13)
    end_hours = random.randint(14, 19)
    month = 10
    day = random.randint(7, 14)
    end_time = f"2023-{month}-{day} {end_hours}:00:00.000"
    start_time = f"2023-{month}-{day} {start_hours}:00:00.000"

    status_index = random.randint(0,1)

    booking_status = status[status_index]
    booking_initiator = initiator[status_index]

    payload = json.dumps({
    "booking_status": booking_status,
    "business_id": "31111727-1de1-4c40-8940-0279eab3f4bb",
    "customer_id": "f51bf997-f79e-4fc5-9299-6e76ff03b070",
    "end_time": end_time,
    "initiator": booking_initiator,
    "services": [
        {
        "service_id": "0e07ee5f-8977-45ae-95b9-6bee42880655",
        "service_variation_id": "6be07ee3-ff71-4583-ad2d-2a550bbf4599"
        }
    ],
    "start_time": start_time,
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code!=200:

        print("fat gaya")
        
    
