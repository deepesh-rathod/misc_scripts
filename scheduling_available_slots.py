import requests
import time

duration = 1
date = "2023-09-14"
business_id = "2cb3a594-7adc-43c7-9093-f366229e5371"


while duration < 100:

    url = f"http://chrone-dev-node-env.eba-t5g6xad2.us-east-1.elasticbeanstalk.com/schedule/bookings/available-slots?business_id={business_id}&date={date}&duration={duration}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code!= 200:
        print("fata")
    else:
        print(duration)
        duration+=1
        time.sleep(1)
        
    

# print(response.text)
