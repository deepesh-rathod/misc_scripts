import requests
import json
import pandas as pd

import requests
import json

url = "https://dashboard.boulevard.io/api/v1.0/graph_client"

payload = json.dumps({
  "query": "query GetMenuCategory($cartId: ID!) {cart(idOrToken: $cartId) {availableCategories{name availableItems{id disabled disabledDescription name description listPriceRange{max min variable}}}}}",
  "variables": {
    "cartId": "6df2218b-1522-4e39-aa2a-2d8188a79c34"
  }
})
headers = {
  'authority': 'dashboard.boulevard.io',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'no-cache',
  'content-type': 'application/json',
  'origin': 'https://dashboard.boulevard.io',
  'pragma': 'no-cache',
  'referer': 'https://dashboard.boulevard.io/booking/businesses/836c11aa-9eaa-4af0-a9fd-a4f7224aab0a/widget',
  'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
  'x-blvd-bid': '836c11aa-9eaa-4af0-a9fd-a4f7224aab0a',
  'x-request-id': 'gh0smdvla-1670933541200'
}

response = requests.request("POST", url, headers=headers, data=payload)

response = response.json()
all_services = []
for cats in response['data']['cart']['availableCategories']:
    for srvc in cats['availableItems']:
        data={
            'service':srvc['name'],
            'description':srvc['description'],
            'price':"$"+str(int(srvc['listPriceRange']['max']/100)),
            'category':cats['name']
        }
        all_services.append(data)

services_df = pd.DataFrame(all_services)
services_df.to_csv("Royalty by rachel services.csv",index=False)


# cat_ids = []
# for cat in res['Categories']:
#     cat_ids.append(cat['Id'])


# all_services = []
# for catid in cat_ids:
#     url = f"https://apiamrs14.zenoti.com/api/Catalog/Services/?categoryId={catid}&centerId=d3683644-b5c1-4760-b4d4-651389b15019&searchString=&page=1&size=100&defaultPage=1&sorters=&defaultSize=100&filters=&NeedsMinMaxPricing=False&FromDeals=False&PostReqServiceId=&PrereqServiceId=&UserMembershipId=&CouplesService=False&parentServiceId=&NeedsPackageBenefitPricing=False"

#     payload={}
#     headers = {
#     'authority': 'apiamrs14.zenoti.com',
#     'accept': 'application/json, text/plain, */*',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,af;q=0.6,zh-CN;q=0.5,zh;q=0.4',
#     'application_name': 'Webstore V2',
#     'application_version': '1.0.0',
#     'authorization': 'bearer AN:royaltybyrachael|$ARD#pXELbdNiZbBjjJrgvh8ZViiolTF8KERNL3l0QsNhyoLeoduxfEpv6YDdrJk4Yd6CYwBch4Eqjks5Ou33t4PuLL4zrhT9qkPJXZ40kgNyky5DGf35Xn1ldl0SY1T+wT3zxGQ9yKGy8zPid96/NXm6qKgLtc17u3H9amyrHJU/QaMFv7NBEb/eWsr7ZpZGhlkqAKl563T5NrTzsMADiodHdyhKse5y5lYGr0QMlK5C8aNxHvPSmLYEKQFwipAJ3KXYSNtpGIQdJeKEWA==',
#     'content-type': 'application/json',
#     'origin': 'https://royaltybyrachael.zenoti.com',
#     'referer': 'https://royaltybyrachael.zenoti.com/',
#     'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
#     'sec-ch-ua-mobile': '?1',
#     'sec-ch-ua-platform': '"Android"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
#     'x-languagecode': 'en-US'
#     }

#     response = requests.request("GET", url, headers=headers, data=payload)
#     srvcs = response.json()['Services']
#     for srv in srvcs:
#         data = {
#             'service':srv['Name'],
#             'description':srv['Description'],
#             'price':"$"+str(int(srv['Price']['Final'])),
#             'category':srv['CategoryName']
#         }
#         all_services.append(data)
#     print("0")

# srvc_df = pd.DataFrame(all_services)
# srvc_df.to_csv("Royalty by Rachel services.csv")
# print("done")

# all_services = []
# categories = []
# for cats in resp['categories']:
#     c = {
#         "cogs_id":cats['cogs_id'],
#         "name":cats['name']
#     }
#     categories.append(c)

# for cat in categories:
#     for srvc in resp['services']:
#         if cat['cogs_id'] == srvc['category_token']:
#             if srvc['price_cents'] is not None:
#                 data = {
#                     "service":srvc['name'],
#                     "price":"$"+str(int(srvc['price_cents']/100)),
#                     "description":srvc['description'],
#                     "category":cat['name']
#                 }
#                 all_services.append(data)
#             else:
#                 data = {
#                     "service":srvc['name'],
#                     "price":"Price Varies",
#                     "description":srvc['description'],
#                     "category":cat['name']
#                 }
#                 all_services.append(data)
#     print("0")
    

# srvc_df = pd.DataFrame(all_services)
# srvc_df.to_csv("Sheila Maries skin.csv")
# print(0)