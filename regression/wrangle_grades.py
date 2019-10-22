import pandas as pd
import numpy as np

def wrangle_grades():
    grades = pd.read_csv("student_grades.csv")
    grades.drop(columns='student_id', inplace=True)
    grades.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df = grades.dropna().astype('int')
    return df