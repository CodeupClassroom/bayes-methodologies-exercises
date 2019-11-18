from os import path

import requests
import pandas as pd
import env

BASE_URL = 'https://python.zach.lol'
API_BASE = BASE_URL + '/api/v1'

def get_store_data_from_api():
    url = API_BASE + '/stores'
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data['payload']['stores'])

def get_item_data_from_api():
    url = API_BASE + '/items'
    response = requests.get(url)
    data = response.json()

    stores = data['payload']['items']

    while data['payload']['next_page'] is not None:
        print('Fetching page {} of {}'.format(data['payload']['page'] + 1, data['payload']['max_page']))
        url = BASE_URL + data['payload']['next_page']
        response = requests.get(url)
        data = response.json()
        stores += data['payload']['items']

    return pd.DataFrame(stores)

def get_sale_data_from_api():
    url = API_BASE + '/sales'
    response = requests.get(url)
    data = response.json()

    stores = data['payload']['sales']

    while data['payload']['next_page'] is not None:
        print('Fetching page {} of {}'.format(data['payload']['page'] + 1, data['payload']['max_page']))
        url = BASE_URL + data['payload']['next_page']
        response = requests.get(url)
        data = response.json()
        stores += data['payload']['sales']

    return pd.DataFrame(stores)

def get_store_data(use_cache=True):
    if use_cache and path.exists('stores.csv'):
        return pd.read_csv('stores.csv')
    df = get_store_data_from_api()
    df.to_csv('stores.csv', index=False)
    return df


def get_item_data(use_cache=True):
    if use_cache and path.exists('items.csv'):
        return pd.read_csv('items.csv')
    df = get_item_data_from_api()
    df.to_csv('items.csv', index=False)
    return df

def get_sale_data(use_cache=True):
    if use_cache and path.exists('sales.csv'):
        return pd.read_csv('sales.csv')
    df = get_sale_data_from_api()
    df.to_csv('sales.csv', index=False)
    return df

def get_all_data():
    sales = get_sale_data()
    items = get_item_data()
    stores = get_store_data()

    sales = sales.rename(columns={'item': 'item_id', 'store': 'store_id'})

    return sales.merge(items, on='item_id').merge(stores, on='store_id')

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_store_data_sql(cache=True):
    csv_file_path = './store_item_demand.csv'

    query = '''
    SELECT
        sales.*,
        items.item_brand,
        items.item_name,
        items.item_price,
        stores.store_address,
        stores.store_zipcode,
        stores.store_city,
        stores.store_state
    FROM sales
    JOIN items USING(item_id)
    JOIN stores USING(store_id)
    '''

    if cache and path.exists(csv_file_path):
        return pd.read_csv(csv_file_path)
    else:
        df = pd.read_sql(query, get_connection('tsa_item_demand'))
        df.to_csv(csv_file_path, index=False)
        return df

def get_opsd_data(use_cache=True):
    if use_cache and path.exists('opsd.csv'):
        return pd.read_csv('opsd.csv')
    df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    df.to_csv('opsd.csv', index=False)
    return df

