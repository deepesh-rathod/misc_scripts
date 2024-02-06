import pandas as pd
from collections import defaultdict
import json

data_df = pd.read_csv('/Users/office/Documents/scheduling_business_details.csv')

biz_names = []

data_df.dropna(subset='Email',inplace=True)
print(0)
