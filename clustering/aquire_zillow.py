#Zillow
#Create a file nameed `aquire_zillow.py` that will contain functions that do the following
#1) Open a connection to a mySQL database.The name of the database should be in the input to this function
#Make sure your database credentials are not included in this file.
import pandas as pd
import env
def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
#2)Query the zillow database and return a single dataframe
#Make sure to include the logerror and all fields related to the properties that are availabile
#However,for those id variables that have a reference table that holds the description,
#such as `airconditioniningtypeid` and the table `airconditioningtype`,
#include the descriptions of those fields but do not include the id column in your output.
#That is,you would include `airconditioningtypedesc` and not `airconditioningid`
#You will end up using all the tables in the database
# Be sure to do the correct join. We do not want to eliminate properties purely
# because they have a null value for `airconditioningtypeid` 
#only include properties with a transaction in 2016 &/or 2017 along with zestimate error and date of transaction
#only include properties that include a latitude and longitude value
zillow_sql='''
USE zillow;
SELECT 
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





#3)Save the dataframe as a .csv file locally.
#Test these functions by creating a seperate jupyter notebook,importing your `acquire` module
#and calling the functions in it
df_zillow=get_zillow_data()
df_zillow.to_csv("zillow_df.csv")
