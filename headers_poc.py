home_section = [
    {
        "id":110,
        "name": "header",
        "type": "header"
    },
    {
        "id":131,
        "name": "Home",
        "type": "banner"
    },
    {
        "id":137,
        "name": "About Us",
        "type": "working_hrs"
    },
    {
        "id":134,
        "name": "Services",
        "type": "category"
    },
    {
        "id":116,
        "name": "Gallery",
        "type": "gallery"
    },
    {
        "id":115,
        "name": "Testimonials",
        "type": "testimonials"
    },
    {
        "id":138,
        "name": "Contact Us",
        "type": "contact_form"
    },
    {
        "id":117,
        "name": "FAB",
        "type": "fab_mobile"
    },
    {
        "id":133,
        "name": "footer",
        "type": "footer"
    }
]



header_links = []
for section in home_section:
    if section['type'] not in ['header', 'footer', 'fab_mobile', 'contact_form', 'media_preview', 'offer_card', 'blog_preview']:
        header_links.append({
            "name":section['name'],
            "link":section['type']
        })

print(header_links)