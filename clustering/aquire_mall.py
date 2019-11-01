#Mall customers
#Create a file named `aquire_mall.py` that contains a function that
#returns the data from the `customers` table in the `mall_customers` database.
import pandas as pd
import env
def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_mall_data():
    return pd.read_sql('SELECT * FROM customers',get_connection('mall_customers'))  

