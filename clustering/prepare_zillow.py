import pandas as pd
import scipy.stats as stats
import numpy as np
from aquire_zillow import get_zillow_data 

""" Remove any properties that are likely to be something other than single unit properties.
(e.g. no duplexes, no land/lot, ...). 
There are multiple ways to estimate that a property is a single unit, and there is not a single "right" answer. But for this exercise, do not purely filter by unitcnt as we did previously. Add some new logic that will reduce the number of properties that are falsely removed.
You might want to use bedrooms, square feet, unit type or the like to then identify those with unitcnt not defined.

 """
def zillow_single_unit(df):
    criteria_1=df.propertylandusedesc=='Single Family Residential'
    #criteria_2=df.unitcnt==1 | df.unitcnt.isna()
    #criteria_2=df.unitcnt==1 & calculatedfinishedsquarefeet>500
    criteria_2=df.calculatedfinishedsquarefeet>500
    df=df[(criteria_1) & (criteria_2)]
    return df

""" Create a function that will drop rows or columns based on the percent of values that are missing: handle_missing_values(df, prop_required_column, prop_required_row).

The input:
A dataframe
A number between 0 and 1 that represents the proportion, for each column, of rows with non-missing values required to keep the column. i.e. if prop_required_column = .6, then you are requiring a column to have at least 60% of values not-NA (no more than 40% missing).
A number between 0 and 1 that represents the proportion, for each row, of columns/variables with non-missing values required to keep the row. For example, if prop_required_row = .75, then you are requiring a row to have at least 75% of variables with a non-missing value (no more that 25% missing).
The output:
The dataframe with the columns and rows dropped as indicated. Be sure to drop the columns prior to the rows in your function.
hint:
Look up the dropna documentation.
You will want to compute a threshold from your input values (prop_required) and total number of rows or columns.
Make use of inplace, i.e. inplace=True/False. """

def remove_columns(df, cols_to_remove):
    df = df.drop(columns=cols_to_remove)
    return df

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .60):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df



""" 3)Decide how to handle the remaining missing values:
Fill with constant value.
Impute with mean, median, mode.
Drop row/column """

def fill_missing_values(df,fill_value):
    df.fillna(fill_value)
    return df
