import json
import requests

def send_justcall_sms(message, recipient, media_url=None):
    try:
        phone = (
            str(recipient)
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")[-10:]
        )
        message = message

        if media_url is not None:

            payload = {"from": "+12155150601", "to": phone, "body": message, "media_url":media_url}
        else:
            payload = {"from": "+12155150601", "to": phone, "body": message}

        headers = {
            "Accept": "application/json",
            "Authorization": "4b5dfa5e509f02bfd0bea03c553f0ba6184b45a8:86455c6ef23f93eba1ed7b967f9f8def5564af24",
        }

        options = {"headers": headers, "data": json.dumps(payload)}

        response = requests.post("https://api.justcall.io/v1/texts/new", **options)
        result = response.json()

        print(result)

        data_json = {
            "message_id": str(result["id"]),
            "phone": recipient,
            "message": message,
        }
        print("MESSAGE SENT SUCCESSFULL")
        return result

    except Exception as e:

        data_json = {
            "status": "error : could not send msg",
            "error": str(e),
            "message": message,
        }
        print("MESSAGE SENT ERROR")
        return data_json
    
def send_callhippo_sms(message, recipient):
    try:

        phone = (
            str(recipient)
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")[-10:]
        )
        phone = "+1" + phone
        message = message

        payload = {"from": "+18145594564", "to": phone, "userEmail": "kritwish@timelyai.com", "smsBody": message}

        headers = {
        'apiToken': '64b03b912980381596ee26f4',
        'Content-Type': 'application/json',
        'User-Agent':'PostmanRuntime/7.35.0'
        }

        options = {"headers": headers, "data": json.dumps(payload)}

        response = requests.post("https://web.callhippo.com/v1/sms/send", **options)
        result = response.json()

        data_json = {
            "message_id": str(result["id"]),
            "phone": recipient,
            "message": message,
        }


    except Exception as e:

        data_json = {
            "status": "error : could not send msg",
            "error": str(e),
            "message": message,
        }

        return data_json


# send_callhippo_sms("This is a test message from call hippo","8485653917")
send_justcall_sms("Message from python function","8485653917","https://chrone-sp-website.s3.amazonaws.com/icons/bottomSheetImage.png")