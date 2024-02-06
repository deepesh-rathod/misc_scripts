import requests
import json
# from common.slack import send_slack_notification

def get_deal_id(place_id):
    custom_field_value = place_id

    url = f"https://api.pipedrive.com/v1/deals/search?term={place_id}&start=0&api_token=48d67d6ad10fc4b4634dbfce79cc8ebc9512e529"

    response = requests.get(url)

    if response.status_code == 200:
        if len(response.json()['data']['items'])!=0:
            deal_id = response.json()['data']['items'][0]['item']['id']
            return deal_id
        else:
            return None
    else:
        return None


def update_deal(deal_id=None,field=None,value=None,place_id=None):
    
    if place_id is None:
        # send_slack_notification("Error : Invalid request\nPlace id not given","website-pipedrive-alerts")
        print("Error : Invalid request\nPlace id not given")
    else:
        deal_id = get_deal_id(place_id)

    if deal_id is None or field is None or value is None:
        # send_slack_notification("Error : Invalid request\nCould not find deal","website-pipedrive-alerts")
        print("Error : Invalid request\nCould not find deal")
    else:
        url = f"https://api.pipedrive.com/v1/deals/{deal_id}?api_token=48d67d6ad10fc4b4634dbfce79cc8ebc9512e529"

        payload = json.dumps({
            field: value
        })

        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cookie': '__cf_bm=aqTqcj7oNLf6UJyTaSCFa1ra_srNoAIesIAy0iZKEZM-1683714125-0-AUmkAs5KBYBCibuhaYXjCN3er7dgrnqvOuShtPlwYoZHQervBgHeWYjaslnYkSFDsGJrcglR1IjuwcDwbi7i8RQ='
        }

        update_deal_response = requests.request("PUT", url, headers=headers, data=payload)
        print(update_deal_response.text)

        if update_deal_response.status_code != 200:
            print("Error : Invalid request\nCould not find deal")
            # send_slack_notification("Error : Invalid request\nCould not update website url","website-pipedrive-alerts")


update_deal(field="ed9f22b00c69327c9ea6337505eced967a98bcc2",value="https://oops-upside-yo-head.chrone.work/",place_id="ChIJWU1NdC6VQIYRyIQ1SasjmuY")