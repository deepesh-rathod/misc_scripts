import requests
import json

def is_website_banner(banner_type):
    if(banner_type and banner_type=='website'):
        return True
    else:
        return False
    
def is_valid_height(height):
    if height and float(height)<=1:
        return True
    else:
        return False
    
def is_valid_template(template_path):
    if template_path and template_path != 'null' and 'null' not in template_path and 'banner' in template_path:
        return True
    else:
        return False

def is_valid_null_case(template_path,banner_height):
    if template_path==None and float(banner_height)==0:
        return True
    else:
        return False
    
def check_banner_render(banner_url):
    banner_resp = requests.get(banner_url)
    if banner_resp.status_code != 200:
        return False
    else:
        return True
    
data = None
with open('app_uids.json', 'r') as file:
    data = json.load(file)

uids = [d.get("uid") for d in data]

# uids = ["1fc1c04f-8ab6-4bb0-abe1-6c5938df94e4"]

node_url = "https://timely.work/"

results = []

for uid in uids:
    result_data = {"uid":uid}
    url = f"https://timely.work/banner/banner-details?uid={uid}"

    resp = requests.get(url)

    if(resp.status_code!=200):
        print("fata")
        result_data["fetch_banner"]="ERROR"
    else:
        result_data["fetch_banner"]="SUCCESS"
        banner_details = resp.json()
        for _,screen in enumerate(banner_details):
            banners = banner_details.get(screen)
            for banner in banners:

                banner_type = banner.get("type")
                banner_template_path = banner.get('template_path')
                banner_height = banner.get('height')
                if is_website_banner(banner_type):
                    if is_valid_template(banner_template_path) and is_valid_height(banner_height):
                        if banner_template_path[0] == "/":
                            banner_template_path = banner_template_path[1:]
                        banner_url = node_url+banner_template_path
                        if check_banner_render(banner_url):
                            print(f"SUCCESS : {banner_type} success")
                            result_data[banner_type]="SUCCESS"
                        else:
                            result_data[banner_type]="ERROR"
                            print(f"ERROR : rendering {banner_type} banner error")
                    else:
                        
                        if is_valid_null_case(banner_template_path,banner_height):
                            print(f"SUCCESS : {banner_type} will not render")
                            result_data[banner_type]="SUCCESS"
                        else:
                            print(f"ERROR : {banner_type} banner fata")
                            result_data[banner_type]="ERROR"
                else:
                    if is_valid_template(banner_template_path):
                        banner_url = node_url+banner_template_path
                        if check_banner_render(banner_url):
                            print(f"SUCCESS : {banner_type} success")
                            result_data[banner_type]="SUCCESS"
                        else:
                            print(f"ERROR : rendering {banner_type} banner error")
                            result_data[banner_type]="ERROR"
                    else:
                        print(f"ERROR : {banner_type} banner fata")
                        result_data[banner_type]="ERROR"
                
    results.append(result_data)

file_name = "app_banner_qc_result.json"
with open(file_name, 'w') as file:
    json.dump(results, file)