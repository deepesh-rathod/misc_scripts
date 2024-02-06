import pandas as pd
import json

business_names = ["The Art of Slay",
"Perfect Tan",
"Lanex Beauty Center",
"Esthetic Style Spa",
"Celebrity Beauty Waxing and More",
"Bare Cheeks Aesthetics"]

raw_data_df = pd.read_csv('/Users/office/lambdas-prod/profile_completion/scrape_services/merged_result.csv')

# for i in range(raw_data_df.shape[0]):
#     row = raw_data_df.iloc[i]

#     old_services = json.loads(row['old_services'])
#     new_services = json.loads(row['new_services'])
    
#     old_service_names = []
#     new_service_names = []

#     for category in old_services:
#         services = [srvc['name'] for srvc in category['services']]
#         old_service_names.append(services)

#     for category in new_services:
#         services = [srvc['name'] for srvc in category['services']]
#         new_service_names.append(services)

#     if new_service_names != old_service_names:
#         raw_data_df.loc[raw_data_df.index[i], 'services_changed'] = True
#     else:
#         raw_data_df.loc[raw_data_df.index[i], 'services_changed'] = False

# print(0)

uids = []

i=0
for name in business_names:
    temp_file_name = name.lower().replace(" ","_") + ".csv"
    row = raw_data_df[raw_data_df['file_name']==temp_file_name]
    uids.append(row['uid'].values[0])
    print(0)
print(0)
