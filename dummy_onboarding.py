import requests

business_ids = ('1153f1ac-3786-4863-a296-2ef8445b6cb9', 'e2ad873d-c765-49c9-9cca-972a908ff348', '010ebf3e-4ac7-478b-a3a6-6591bf1c280b', 'ff7eccc5-f52b-4cd2-8835-abc4e158472d', '1d6edd65-d3b2-4e99-aef0-2422e47c3231', '11f598d3-af3d-4197-b79a-5ddcbc6d8728', 'fb061a7a-9555-4208-8cc4-125d23cd0c14')

for id in business_ids:
    url = f"http://chrone-dev-node-env.eba-t5g6xad2.us-east-1.elasticbeanstalk.com/schedule/onboard?id={id}"

    payload = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    if(response.status_code!=200):
        print("sab fat gya")
    else:
        print("business onboarded successfully")

    print(response.json())
