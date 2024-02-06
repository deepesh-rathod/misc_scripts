import pandas as pd
import sys
import os

path = "c:\\Users\\D01\\Documents\\timelyAI\\sp_website"
dir_list = os.listdir(path)

writer = pd.ExcelWriter('all services.xlsx') # Arbitrary output name
for file in dir_list:
    if file.endswith('.csv'):
        df = pd.read_csv(file)
        df.to_excel(writer,sheet_name=file)
writer.save()