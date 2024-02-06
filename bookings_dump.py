import pandas as pd
from sqlalchemy import create_engine

HOST="db-prod.cn908eifui4f.us-east-1.rds.amazonaws.com"
PORT="5432"
USER="postgres"
REGION="us-east-1c"
DB_NAME="postgres"
PASS = "March2021"

def init_rds():
    cluster_endpoint = f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}"
    engine = create_engine(cluster_endpoint)
    return engine
conn = init_rds()

dummy_data_df = pd.read_csv("/Users/office/Documents/bookings_dump.csv")

dummy_data_df['start_time'] = pd.to_datetime(dummy_data_df['start_time'], format='%d/%m/%Y %H:%M')



# dummy_data_df.to_csv("dummy_bookings.csv",index=False)

# print(0)

table_name = 'bookings_dev'
dummy_data_df.to_sql(name=table_name, con=conn, if_exists='append', index=False, schema="scheduling")

print(0)

