import requests
import json
import re

def fresha_services(url):
    services = []
    try:
        if "menu=true" not in url:
            url = url + "?menu=true"
            response = requests.get(url)
            html_content = response.text
            start = html_content.find('<script type="application/ld+json">')
            end = html_content.find('</script>', start)
            json_data = html_content[start:end].strip()
            json_data = re.sub('<.*?>', '', json_data)
            data = json.loads(json_data)
            has_offer_catalog = data.get('hasOfferCatalog')
            pattern = r'<p data-qa="category-name".*?>(.*?)</p>'
            category_names = re.findall(pattern, html_content, re.DOTALL)
            cnt = 0
            if has_offer_catalog:
                items = has_offer_catalog.get('itemListElement')
                for temp in items:
                    for item in temp:
                        offered = item.get('itemOffered', {})
                        name = offered.get('name')
                        description = offered.get('description')
                        price = item.get('price')
                        result = {
                            "name": name,
                            "price": "$"+str(price),
                            "description": description,
                            "category":category_names[cnt]
                        }
                        services.append(result)
                    cnt+=1
                return services
            else:
                return services
    except Exception as e:
        print("ERROR : ",e)
        return services

services = fresha_services("https://www.fresha.com/a/michelles-massage-spa-phoenix-3375-east-shea-boulevard-5nwjyk8f")
print(services)