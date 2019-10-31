
import pandas as pd
import scipy.stats as stats
import numpy as np

def remove_columns(df, cols_to_remove):
    df = df.drop(columns=cols_to_remove)
    return df

# handle_missing_values(df, prop_required_column, prop_required_row).  
#   - The input: a dataframe, a number between 0 and 1 that represents the proportion, for each column, of rows with non-missing values required to keep the column.  i.e. if prop_required_column = .6, then you are requiring a column to have at least 60% of values not-NA (no more than 40% missing), a number between 0 and 1 that represents the proportion, for each row, of columns/variables with non-missing values required to keep the row.  i.e. if prop_required_row = .75, then you are requiring a row to have at least 75% of variables with a non-missing value (no more that 25% missing) 
#   - The output: the dataframe with the columns and rows dropped as indicated. *Be sure to drop the columns prior to the rows in your function.*


def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

# Create a function that fills missing values with 0s where it makes sense based on the attribute/field/column/variable. 

def fill_zero(df, cols):
    df.fillna(value=0, inplace=True)
    return df


def data_prep(df, cols_to_remove=[], prop_required_column=.5, prop_required_row=.75):
    df = remove_columns(df, cols_to_remove)
    df = handle_missing_values(df, prop_required_column, prop_required_row)
    return df

# Data types: Write a function that takes in a dataframe and a list of columns names and returns the dataframe with the datatypes of those columns changed to a non-numeric type & use this function to appropriately transform any numeric columns that should not be treated as numbers
def numeric_to_category(df, cols):
    df[cols] = df[cols].astype('category')
    return df

# Write a function that accepts the zillow data frame and removes the outliers. 
def remove_outliers_iqr(df, columns):
    for col in columns:
        q75, q25 = np.percentile(df[col], [75,25])
        ub = 3*stats.iqr(df[col]) + q75
        lb = q25 - 3*stats.iqr(df[col])
        df = df[df[col] <= ub]
        df = df[df[col] >= lb]
    return df