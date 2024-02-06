import requests
import json

def get_square_up_url(url):
    try:
        url_part = url.split("/")[2]
        square_id_url = f"https://{url_part}/ajax/api/JsonRPC/Commerce/?Commerce/\\[Checkout::getSquareStoreConfig\\]"
        payload = json.dumps({
        "id": 0,
        "jsonrpc": "2.0",
        "method": "Checkout::getSquareStoreConfig",
        "params": []
        })
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        response = requests.request("POST", square_id_url, headers=headers, data=payload)
        square_id = json.loads(response.text)['result']['locations'][0]['square_location_id']

        square_appointment_url=f'https://squareup.com/appointments/book/{square_id}/services'
        response = requests.request("GET", square_appointment_url)
        final_url = response.url
        return {"res":True,"url":final_url}
    except Exception as e:
        return {"res":False,"error":e}

def square_services(url):
    services = []
    try:
        p_url = url
        if "square.site" in p_url.split("/")[2]:
            resp = get_square_up_url(url)
            if resp['res']==True:
                p_url = resp['url']
            else:
                print("Error : ",resp['error'])
                return services
        lst = p_url.split("/")

        url = f"https://squareup.com/appointments/api/buyer/widget/{lst[5]}?unit_token={lst[6]}"

        payload={}
        headers = {
          'authority': 'squareup.com',
          'accept': 'application/json, text/javascript, */*; q=0.01',
          'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,af;q=0.6,zh-CN;q=0.5,zh;q=0.4',
          'cookie': '_savt=60d2bd0e-b9e7-4905-a284-41343f88f8b6; squareGeo=GB-BDG; _savt=15204517-22aa-44f0-849b-0705aa28d18f; dajs_user_id=null; dajs_group_id=null; da_js_user_type=%22anonymous_visitor%22; _gcl_au=1.1.152494653.1667983898; _fbp=fb.1.1667983899865.2117643972; OptanonAlertBoxClosed=2022-11-09T08:51:41.180Z; _appointments_session=eWtnanZ1YlczVVZMRTdSa1lSSEl4RzJ5WFh6Ukx1WmducHZDbXJUMVNOakZlYkFYOVpwRjJLSGdwSDlEWmllb0xHZjc2S0dqMldrMFppVlRhOTg4TjRTN1lpZU5EYlpNd2pGZkxEdUd4cUxHdWM5eStaVjNMSGRtcHVrMGxZOXlES1lzTFB1dnk2RWl1aFVaRWd0Mk45cmJ2L1Jub205M0R3NE9tUEhHZ3hZUTVuTktuaTAxYjA3YXM0RHBRRnA5LS03MUlQeTZIV2JsL3J3L3c2VU94SUt3PT0%3D--59729ea6ddb6d73fe8210ca66ecdeae2b7fff3d1; dajs_anonymous_id=%2260d2bd0e-b9e7-4905-a284-41343f88f8b6%22; OptanonConsent=isIABGlobal=false&datestamp=Wed+Nov+09+2022+14%3A21%3A58+GMT%2B0530+(India+Standard+Time)&version=6.39.0&hosts=&consentId=b66e4e24-e199-483d-92c0-d63b3f719b1a&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=GB%3B&AwaitingReconsent=false; squareGeo=IN-MP',
          'referer': 'https://squareup.com/appointments/book/a7ec799rl6rgux/LZDRNEV1X3P52/services',
          'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
          'x-csrf-token': 'eKhKBTys1+Aoog3FnSKBHZb1Jr37BVBsTEU+AlF/Wd2a+XD2iQEkaXASAVqi8I/DxTRV/Cs1URqn/zwEXv7mJw==',
          'x-requested-with': 'XMLHttpRequest'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        resp = response.json()
        api_categories = resp['categories']
        api_services = resp['services']

        for srvc in api_services:
            if srvc['price_cents'] is not None:
                price = "$"+str(int(srvc['price_cents']/100))
            else:
                price = ""
            srv = {
                "name":srvc['name'],
                "description":srvc['description'],
                "price":price,
                "category":"",
            }
            if srvc['category_token'] is not None:
                srv_cat=next(cat['name'] for cat in api_categories if cat['id']==srvc['category_token']),
                srv["category"]=srv_cat[0]
            services.append(srv)
            
        return services
        
    except:
        return services

services = square_services("https://sphynxhairlounge.square.site/s/appointments")
        