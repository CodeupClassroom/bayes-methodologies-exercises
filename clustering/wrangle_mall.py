""" wrangle_mall.py
1)Acquire data from mall_customers.customers in mysql database.
2)Split the data
3)One-hot-encoding
4)Missing values
5)Scaling """

#1
import pandas as pd
from sklearn.model_selection import train_test_split
import env
def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_mall_data():
    return pd.read_sql('SELECT * FROM customers',get_connection('mall_customers'))  

#2)
def split_my_data(df,perc_test,random_seed):
    X_train,X_test=train_test_split(df,test_size=perc_test,random_state=random_seed)
    return X_train,X_test

#3)d
def ohe(cat_var):
    



#4)


#5)
