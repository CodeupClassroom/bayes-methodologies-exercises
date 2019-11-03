#Zillow
#1)Acquire data from mySQL using the python module to connect and query. You will want to end with a single dataframe. Make sure to include: the logerror, all fields related to the properties that are available. You will end up using all the tables in the database.
#Be sure to do the correct join (inner, outer, etc.). We do not want to eliminate properties purely because they may have a null value for airconditioningtypeid.
#Only include properties with a transaction in 2017, and include only the last transaction for each properity (so no duplicate property ID's), along with zestimate error and date of transaction.
#Only include properties that include a latitude and longitude value

import pandas as pd
import env
def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

zillow_sql='''SELECT 
Z.basementsqft,
Z.bathroomcnt,
Z.bedroomcnt,
Z.calculatedbathnbr,
Z.finishedfloor1squarefeet,
Z.calculatedfinishedsquarefeet,
Z.finishedsquarefeet12,
Z.finishedsquarefeet13,
Z.finishedsquarefeet15,
Z.finishedsquarefeet50,
Z.finishedsquarefeet6,
Z.fips,
Z.fireplacecnt,
Z.fullbathcnt,
Z.garagecarcnt,
Z.garagetotalsqft,
Z.hashottuborspa,
Z.latitude,
Z.longitude,
Z.lotsizesquarefeet,
Z.poolcnt,
Z.poolsizesum,
Z.propertycountylandusecode,
Z.propertyzoningdesc,
Z.regionidcity,
Z.regionidcounty,
Z.regionidneighborhood,
Z.regionidzip,
Z.roomcnt,
Z.threequarterbathnbr,
Z.unitcnt,
Z.yardbuildingsqft17,
Z.yardbuildingsqft26,
Z.yearbuilt,
Z.numberofstories,
Z.fireplaceflag,
Z.structuretaxvaluedollarcnt,
Z.taxvaluedollarcnt,
Z.assessmentyear,
Z.landtaxvaluedollarcnt,
Z.taxamount,
Z.taxdelinquencyflag,
Z.taxdelinquencyyear,
Z.censustractandblock,
unique_properties.logerror,
unique_properties.transactiondate,
plt.propertylandusedesc,
st.storydesc,
ct.typeconstructiondesc,
act.airconditioningdesc,
bct.buildingclassdesc,
hst.heatingorsystemdesc
FROM 
(SELECT 
p17.parcelid,
logerror,
transactiondate
FROM 
predictions_2017 AS p17
JOIN
(SELECT 
predictions_2017.parcelid,
MAX(transactiondate) AS max_trans_date
FROM predictions_2017
GROUP BY predictions_2017.parcelid) AS pred_agg ON (p17.parcelid=pred_agg.parcelid) AND (pred_agg.max_trans_date=p17.transactiondate)) AS unique_properties
LEFT JOIN properties_2017 AS Z ON (Z.parcelid=unique_properties.parcelid)
LEFT JOIN propertylandusetype AS plt ON (Z.propertylandusetypeid=plt.propertylandusetypeid)
LEFT JOIN storytype AS st ON (Z.storytypeid=st.storytypeid)
LEFT JOIN typeconstructiontype AS ct ON (Z.typeconstructiontypeid=ct.typeconstructiontypeid)
LEFT JOIN airconditioningtype AS act ON (Z.airconditioningtypeid=act.airconditioningtypeid)
LEFT JOIN architecturalstyletype AS ast ON (Z.architecturalstyletypeid=ast.architecturalstyletypeid)
LEFT JOIN buildingclasstype AS bct ON (Z.buildingclasstypeid=bct.buildingclasstypeid)
LEFT JOIN heatingorsystemtype AS hst ON (Z.heatingorsystemtypeid=hst.heatingorsystemtypeid)
WHERE Z.latitude IS NOT NULL AND Z.longitude IS NOT NULL '''
def get_zillow_data():
    return pd.read_sql(zillow_sql,get_connection('zillow'))



# 2)Summarize your data (summary stats, info, dtypes, shape, distributions, value_counts, etc.)  
def df_value_counts(df):
    counts = pd.Series([])
    for _, col in enumerate(df.columns.values):
        if df[col].dtype == 'object':
            col_count = df[col].value_counts()
        else:
            col_count = df[col].value_counts(bins=10, sort=False)
        counts = counts.append(col_count)
    return counts

def df_summary(df):
    print('--- Info')
    df.info()
    print('--- Shape: {}'.format(df.shape))
    print('--- Descriptions')
    print(df.describe(include='all'))
    print('--- Value Counts')
    print(df_value_counts(df))


""" 3)Write a function that takes in a dataframe of observations and attributes and returns a dataframe
where each row is an atttribute name, the first column is the number of rows with missing values for that attribute,
and the second column is percent of total rows that have missing values for that attribute. 
Run the function and document takeaways from this on how you want to handle missing values    
 """


def nulls_by_col(df):
    num_missing = df.isnull().sum()
    rows = df.shape[0]
    pct_missing = num_missing/rows
    cols_missing = pd.DataFrame({'num_rows_missing': num_missing, 'pct_rows_missing': pct_missing})
    return cols_missing

def print_nulls_by_column(df):
    print('--- Nulls By Column')
    print(nulls_by_col(df))


"""1) Write a function that takes in a dataframe and returns a dataframe with 3 columns: the number of columns missing, percent of columns missing, and number of rows with n columns missing. Run the function and document takeaways
from this on how you want to handle missing values. """

def nulls_by_row(df):
    num_cols_missing = df.isnull().sum(axis=1)
    pct_cols_missing = df.isnull().sum(axis=1)/df.shape[1]*100
    rows_missing = pd.DataFrame({'num_cols_missing': num_cols_missing, 'pct_cols_missing': pct_cols_missing}).reset_index().groupby(['num_cols_missing','pct_cols_missing']).count().rename(index=str, columns={'index': 'num_rows'}).reset_index()
    return rows_missing 

def print_nulls_by_row(df):
    print('--- Nulls By Row')
    print(nulls_by_row(df))
