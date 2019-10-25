#Do your work for this in a file named `prepare`.
#1)Use the function defined in `aquire.py` to load the iris data.

import pandas as pd
import numpy as np
import scipy as sp 

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler


def rename_columns(df):
    df['species']=df['species_name']
    return df

def split(df, target, train_prop, seed):
    return train_test_split(df, train_size=train_prop, stratify=df[target], random_state=seed)

def impute(train, test, my_strategy, column_list):
    imputer = SimpleImputer(strategy=my_strategy)
    train[column_list] = imputer.fit_transform(train[column_list])
    test[column_list] = imputer.transform(test[column_list])
    return train, test, imputer

def encode(train, test, col_name):
    encoded_values = sorted(list(train[col_name].unique()))
    
    # Integer Encoding
    int_encoder = LabelEncoder()
    train.encoded = int_encoder.fit_transform(train[col_name])
    test.encoded = int_encoder.transform(test[col_name])
    
    # create 2D np arrays of the encoded variable (in train and test)
    train_array = np.array(train.encoded).reshape(len(train.encoded),1)
    test_array = np.array(test.encoded).reshape(len(test.encoded),1)

    # One Hot Encoding
    ohe = OneHotEncoder(sparse=False, categories='auto')
    train_ohe = ohe.fit_transform(train_array)
    test_ohe = ohe.transform(test_array)
    
    # Turn the array of new values into a data frame with columns names being the values
    # and index matching that of train/test
    # then merge the new dataframe with the existing train/test dataframe
    train_encoded = pd.DataFrame(data=train_ohe,
                            columns=encoded_values, index=train.index)
    train = train.join(train_encoded)
    test_encoded = pd.DataFrame(data=test_ohe,
                               columns=encoded_values, index=test.index)
    test = test.join(test_encoded)
    return train, test, int_encoder, ohe

def scale_minmax(train, test, column_list):
    scaler = MinMaxScaler()
    column_list_scaled = [col + '_scaled' for col in column_list]
    train_scaled = pd.DataFrame(scaler.fit_transform(train[column_list]), 
                                columns = column_list_scaled, 
                                index = train.index)
    train = train.join(train_scaled)
    test_scaled = pd.DataFrame(scaler.transform(test[column_list]), 
                                columns = column_list_scaled, 
                                index = test.index)
    test = test.join(test_scaled)
    return train, test, scaler

def prepare(df, drop_cols, target, train_prop, seed, impute_cols, impute_strategy, encode_col, scale_cols):
    df.fillna(np.nan, inplace=True)
    df.drop(columns=drop_cols, inplace=True)
    train, test = split(df=df, target=target, train_prop=train_prop, seed=seed)
    train, test, imputer = impute(train, test, my_strategy=impute_strategy, column_list=impute_cols)
    train, test, int_encoder, ohe = encode(train, test, col_name = encode_col)
    train, test, scaler = scale_minmax(train, test, column_list = scale_cols)
    return df, train, test, imputer, int_encoder, ohe, scaler