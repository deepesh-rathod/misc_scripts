import requests


# uids = ('08d58fe9-c2ce-44af-bdec-14a145e19d54',
# '0b88497e-fad2-44b8-ac2d-10a56c2b47ff',
# '8f74162f-8d18-40c9-b871-cb628844e8f2',
# 'e8c60929-e707-40a6-b688-fc4e53e6156a')

success_uids = []
failed_uids = []

uids = ('0b88497e-fad2-44b8-ac2d-10a56c2b47ff',)

for uid in uids:
    
    # url_onboard = f"https://timely.work/schedule/onboard?id={uid}"
    # url_opt_in = f"https://timely.work/schedule/opt-in?id={uid}"
    url_get_started = f"https://timely.work/schedule/get-started?id={uid}"

    payload = {}
    headers = {}

    response = requests.request("PUT", url_get_started, headers=headers, data=payload)

    if(response.status_code!=200):
        print("fata")
        failed_uids.append(uid)
    else:
        success_uids.append(uid)
        print(response.json())
        print("done")

print(0)