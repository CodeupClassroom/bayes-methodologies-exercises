from __future__ import division
import itertools
import warnings
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import math
from sklearn import metrics
from random import randint

def aquire():
    colnames=['ip', 'timestamp', 'request_method', 'status', 'size',
              'destination', 'request_agent']
    df_orig = pd.read_csv('http://python.zach.lol/access.log',          
                     engine='python',
                     header=None,
                     index_col=False,
                     names=colnames,
                     sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
                     na_values='"-"',
                     usecols=[0, 3, 4, 5, 6, 7, 8]
    )

    new = pd.DataFrame([["95.31.18.119", "[21/Apr/2019:10:02:41+0000]", 
                         "GET /api/v1/items/HTTP/1.1", 200, 1153005, np.nan, 
                         "python-requests/2.21.0"],
                        ["95.31.16.121", "[17/Apr/2019:19:36:41+0000]", 
                         "GET /api/v1/sales?page=79/HTTP/1.1", 301, 1005, np.nan, 
                         "python-requests/2.21.0"],
                        ["97.105.15.120", "[18/Apr/2019:19:42:41+0000]", 
                         "GET /api/v1/sales?page=79/HTTP/1.1", 301, 2560, np.nan, 
                         "python-requests/2.21.0"],
                        ["97.105.19.58", "[19/Apr/2019:19:42:41+0000]", 
                         "GET /api/v1/sales?page=79/HTTP/1.1", 200, 2056327, np.nan, 
                         "python-requests/2.21.0"]], columns=colnames)

    df = df_orig.append(new)
    return df

def prep():
    df = aquire()

    # set timestamp
    df.timestamp = df.timestamp.str.replace(r'(\[|\])', '', regex=True)
    df.timestamp= pd.to_datetime(df.timestamp.str.replace(':', ' ', 1)) 
    df = df.set_index('timestamp')

    # cleanup text
    for col in ['request_method', 'request_agent', 'destination']:
        df[col] = df[col].str.replace('"', ' ')
    
    df['request_method'] = df.request_method.str.replace(r'\?page=[0-9]+', '', regex=True)
    df['size_mb'] = [n/1024/1024 for n in df['size']]
    return df
