import requests

try:
    # utm_test_string = "?utm_source=test&utm_medium=test&utm_campaign=test"
    # base_url=r[0:-1][0] if r[0][-1]=='/' else r[0]
    # test_service_url =f'{base_url}/services/0'
    # test_service_utm_url = test_service_url + utm_test_string
    response = requests.get("https://red-chair-salon.chroneweb.com/services/0?utm_source=test&utm_medium=test&utm_campaign=test")
    r = "https://red-chair-salon.chroneweb.com/services/0?utm_source=test&utm_medium=test&utm_campaign=test"
    # print(f"{r[0]} - {response.url}")
    if response.status_code!=200 or r.split("https://")[1].split(".")[0] not in response.url:
        print(0)
    # failed_url.append(test_service_utm_url)
except Exception as e:
    # failed_url.append(test_service_utm_url)
    print(0)