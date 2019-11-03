#Functions of the work above needed to aquire and prepare
#a new sample of data
from aquire_zillow import get_zillow_data
from prepare_zillow import zillow_single_unit
from prepare_zillow import remove_columns
from prepare_zillow import handle_missing_values
from prepare_zillow import fill_missing_values

def wrangle_zillow_data():
    df=get_zillow_data()
    df=zillow_single_unit()
    df=handle_missing_values(df)
    return df