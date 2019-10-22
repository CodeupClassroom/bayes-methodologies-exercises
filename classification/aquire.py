#Do your work for these exercises in a file named aquire.
# Use the pydataset module to load the iris data set into a dataframe,`df_iris`
#1a)Print the first 3 rows
from pydataset import data
df_iris=data('iris')
print(df_iris.head(n=3))
#1b)Print the number of rows and columns (shape)
print(df_iris.shape)
#1c)Print the column names
print(df_iris.columns)
#1d)Print the data type of each column
print(df_iris.dtypes)
#1e)Print the summary statistics for each of the numeric variables. Would you recommend rescaling
#the data based on these statistics?
df_iris.describe()
#I would not recommend scaling because values are all on the same scale.

# 2)Read the data tab from the stats module dataset,`Excel_Stats.xlsx`,into a dataframe,
#`df_excel`
import pandas as pd
df_excel=pd.read_excel('Excel_Stats_Instructor.xlsx','Data')
#2a)assign the first 100 rows to a new dataframe,`df_excel_sample`
df_excel_sample=df_excel[0:101]
print(df_excel_sample)
#2b)Print the number of rows of your original dataframe
df_excel.shape[0]
#2c)Print the first 5 column names
print(df_excel.columns[0:5])
#2d)Print the column names that have a data type of object
print(list(df_excel.dtypes[df_excel.dtypes=='object'].index))
num_cols=list(df_excel.dtypes[df_excel.dtypes!='object'].index)
#2e)Compute the range for each of the numeric variables
print(df_excel[num_cols].max()-df_excel[num_cols].min())
#3)Find the train.csv file shared through classroom in topic 'Classification'.Get the contents
# of this file into a dataframe labled `df_google`
df_google=pd.read_csv('train.csv')
#3a)print the first 3 rows
print(df_google.head(n=3))
#3b)print the number of rows and columns
print(df_google.shape)
#3c)print the columnn names
print(df_google.columns)
#3d)print the summary statistics for each numeric variable
df_google.describe()
#3e)print the unique values for each categorical variable. If there are more than 5
#distinct values,print the top 5 in terms of prevelence or frequency
for col in df_google:
    if df_google[col].dtype=='O':
       print(df_google[col].value_counts()[0:5])

#4) In mysql workbench or a terminal, write a query to select all the columns of the passengers
# table from the titanic database.Export the table to a csv you store locally. Read the csv into
# a datafrane `df_csv`
#USE titanic_db;
#SELECT * FROM passengers;  
df_csv=pd.read_csv('passengers.csv')
#4a)Print the head and tail of your new dataframe
#4b)Print the number of rows and columns
print(df_csv.shape)
#4c)Print the column names
print(df_csv.columns)
#4d)Print the summary statistics for each numeric variable
print(df_csv.describe())
#4e)print the unique values for each categorical variables. 
# If there are more than 5 distinct values, 
# print the top 5 in terms of prevelence or frequency.
for col in df_csv:
    if df_csv[col].dtype=='O':
       print(df_csv[col].value_counts()[0:5])
#5) Create a file named `aquire.py` This file should define at least two functions.
#get_titanic_data: returns the titanic data from the codeup data science database as a pandas dataframe
#get_iris_data:returns the data from the `iris_db` on the codeup data science database as a pandas data frame.
#The returned data frame should include the actual name of the species in addition to the species ids. 
#We will use the functions in a later exercise.
import pandas as pd
import env
def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
def get_titanic_data():
    return pd.read_sql('SELECT * FROM passengers',get_connection('titanic_db'))

iris_sql="SELECT measurements.measurement_id,measurements.sepal_length,measurements.sepal_width,measurements.petal_length,measurements.petal_width,species.species_name,species.species_id FROM measurements JOIN species ON(species.species_id=measurements.species_id)"
def get_iris_data():
       return pd.read_sql(iris_sql,get_connection('iris_db'))

