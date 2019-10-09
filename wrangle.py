import pandas as pd
import numpy as np

import env

def get_db_url(db):
    return f'mysql+pymysql://{env.user}:{env.password}@{env.host}/{db}'

def get_data_from_mysql():
    query = '''
    SELECT *
    FROM customers
    JOIN internet_service_types USING (internet_service_type_id)
    WHERE contract_type_id = 3
    '''

    df = pd.read_sql(query, get_db_url('telco_churn'))
    return df

def clean_data(df):
    df = df[['customer_id', 'total_charges', 'monthly_charges', 'tenure']]
    df.total_charges = df.total_charges.str.strip().replace('', np.nan).astype(float)
    df = df.dropna()
    return df
  
def wrangle_telco():
    df = get_data_from_mysql()
    df = clean_data(df)
    return df
    
def wrangle_telco():
    return clean_data(get_data_from_mysql())