import pandas as pd
import env

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

# Remove any properties that are likely to be something other than a single unit properties (e.g. no duplexes, no land/lot, ...). There are multiple ways to estimate that a property is a single unit, and there is not a single "right" answer.

def get_zillow_data():
    query = '''
    SELECT p2.*, p1.logerror FROM predictions_2016 p1
        LEFT JOIN properties_2016 p2  USING(parcelid)
        WHERE (bedroomcnt > 0 AND bathroomcnt > 0 AND calculatedfinishedsquarefeet > 500 
            AND latitude IS NOT NULL AND longitude IS NOT NULL) 
            AND (unitcnt = 1 OR unitcnt IS NULL);
    '''
    return pd.read_sql(query, get_connection('zillow'))

def get_iris_data():
    query = '''
    SELECT petal_length, petal_width, sepal_length, sepal_width, species_id, species_name
    FROM measurements m
    JOIN species s USING(species_id)
    '''
    return pd.read_sql(query, get_connection('iris_db'))

def get_mallcustomer_data():
    df = pd.read_sql('SELECT * FROM customers;', get_connection('mall_customers'))
    return df.set_index('customer_id')