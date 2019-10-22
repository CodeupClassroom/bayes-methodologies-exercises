""" Create split_scale.py that will contain the functions that follow. Each scaler function should create the object, fit and transform both train and test. They should return the scaler, train dataframe scaled, test dataframe scaled. Be sure your indices represent the original indices from train/test, as those represent the indices from the original dataframe. Be sure to set a random state where applicable for reproducibility!
1)split_my_data(X, y, train_pct)
2)standard_scaler()
3)scale_inverse()
4)uniform_scaler()
5)gaussian_scaler()
6)min_max_scaler()
7)iqr_robust_scaler() """

import pandas as pd
from sklearn.preprocessing import StandardScaler, PowerTransformer, MinMaxScaler, RobustScaler, QuantileTransformer
from sklearn.model_selection import train_test_split
import numpy as np

#1. split the data into train and test
def split_my_data(data, train_ratio=.80, seed=123):
    '''the function will take a dataframe and returns train and test dataframe split 
    where 80% is in train, and 20% in test. '''
    return train_test_split(data, train_size = train_ratio, random_state = seed)

# 2. standard_scaler(train, test)

def standard_scaler(train, test):
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

# 3. scale_inverse(scaler, train_scaled, test_scaled)
def my_inv_transform(scaler, train_scaled, test_scaled):
    train = pd.DataFrame(scaler.inverse_transform(train_scaled), columns=train_scaled.columns.values).set_index([train_scaled.index.values])
    test = pd.DataFrame(scaler.inverse_transform(test_scaled), columns=test_scaled.columns.values).set_index([test_scaled.index.values])
    return scaler, train, test

# 4. uniform_scaler(train, test, seed)
def uniform_scaler(train, test, seed=123):
    scaler = QuantileTransformer(n_quantiles=100, output_distribution='uniform', random_state=seed, copy=True).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

# 5. gaussian_scaler(train, test, method)

def gaussian_scaler(train, test, method='yeo-johnson'):
    scaler = PowerTransformer(method, standardize=False, copy=True).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

# 6. min_max_scaler(train, test, minmax_range=0,1)

def my_minmax_scaler(train, test, minmax_range=(0,1)):
    scaler = MinMaxScaler(copy=True, feature_range=minmax_range).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled


# 7. iqr_robust_scaler(train, test)

def iqr_robust_scaler(train, test):
    scaler = RobustScaler(quantile_range=(25.0,75.0), copy=True, with_centering=True, with_scaling=True).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled




