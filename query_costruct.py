values = [
    'banner',
    'blog',
    'blog_preview',
    'blogs',
    'category',
    'category_preview',
    'contact_form',
    'fab_mobile',
    'finance',
    'footer',
    'gallery',
    'header',
    'media_preview',
    'offer_card',
    'partners',
    'products',
    'products_preview',
    'root',
    'schedule',
    'services',
    'stories',
    'testimonials',
    'testmonials_preview',
    'working_hrs'
]

constructed_query = """
"""
# for section in values:
#     query = f"""
#         {section} as (
#     select
#         place_id,path,section->>'id' as {section}
#     from
#         (select place_id,path,i.section as section
#         from gmb_website_details gwd
#         cross join jsonb_array_elements(gwd.sections) as i(section)
#         where gwd.sections::text ilike '%id%') sections
#     where
#         sections::text ilike '%{section}%'
#     ),
#     """
#     constructed_query = constructed_query + query

for section in values:
    query = f"""left join {section} on (gwd.place_id={section}.place_id and gwd.path={section}.path)
    """
    constructed_query = constructed_query + query

# for section in values:
#     query = f"""{section}.{section},
#     """
#     constructed_query = constructed_query + query

('153','148','147','106','55','30','29')


print(0)