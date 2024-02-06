import json
import requests
import pandas as pd

# tone_id = '60ff8d3afc873e000c08e8b2'
# language_id = '607adac76f8fe5000c1e636d'
headers= {'Authentication': 'Bearer KYIPVODH9KBF1LVILJ4NZ', 'Content-Type': 'application/json'}

services = pd.read_csv('jcbeauty..csv')

new_services = []

def service_description(service):
    use_case_id = '60584cf2c2cdaa000c2a7954'
    context = {'SECTION_TOPIC_LABEL': f'What is {service}?'}
    url = 'https://api.rytr.me/v1/ryte'
    data = {"languageId": '607adac76f8fe5000c1e636d', "toneId": '60ff8d3afc873e000c08e8b2', "useCaseId": use_case_id, "inputContexts": context, "variations": 1, "userId": "blah", "format": "text", "creativityLevel": "default"}
    content = requests.post(url, headers=headers, json=data)
    return json.loads(content.text)['data'][0]['text']

for i in range(services.shape[0]):
    row = services.iloc[i]
    desc = service_description(row['Service'])

    new_srvc = {
        'service':row['Service'],
        'description': desc,
        'price':row['Price']
    }

    new_services.append(new_srvc)

new_services_df = pd.DataFrame(new_services)
new_services_df.to_csv("jcbeauty_srvc_desc.csv",index=False)

