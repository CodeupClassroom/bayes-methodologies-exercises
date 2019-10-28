#Do your work for this in a file named `prepare`.
#1)Use the function defined in `aquire.py` to load the iris data.
from acquire import get_iris_data
from acquire import get_titanic_data
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler 
#iris_df=get_iris_data()
#1a) Drop the `species_id` and `measurement_id` columns.
def drop_columns(df):
    return df.drop(columns=['species_id','measurement_id'])
#1b) Rename the `species_name` column to just `species`.
def rename_columns(df):
    df['species']=df['species_name']
    return df
#1c)Encode the species name using a sklearn encoder. Research the inverse_transform method
#of the label encoder.How might this be useful.
def encode_columns(df):
    encoder=LabelEncoder()
    encoder.fit(df.species)
    df.species=encoder.transform(df.species)
    return df
#create a function that accepts the untransformed iris
#data, and returns the data with the transformations above applied.
def prep_iris(df):
    df=df.pipe(drop_columns).pipe(rename_columns).pipe(encode_columns)
    return df 
# Titanic Data
# Use the function you defined in aquire.py to load the titanic data set    
#df=get_titanic_data()
# 2a) Handle the missing values in the `embark_town` and `embarked`columns.
def titanic_missing_fill(df):
    df.embark_town.fillna('Other',inplace=True)
    df.embarked.fillna('Unknown',inplace=True)
    return df
# 2b) Remove the deck column.
def titanic_remove_columns(df):
    return df.drop(columns=['deck'])
# 2c) Use a label encoder to transform the `embarked` column
def encode_titanic(df):
    encoder_titanic=LabelEncoder()
    encoder_titanic.fit(df.embarked)
    df['embarked']=encoder_titanic.transform(df.embarked)
    return df
# 2d) Scale the `age` and `fare` columns using a min/max scaler.
def scale_titanic(df):
    scaled=MinMaxScaler()
    scaled.fit(df[['age','fare']])
    df[['age','fare']]=scaled.transform(df[['age','fare']])
    return df
#Why might this be beneficial? When might this be beneficial? When might you not
#want to do this?
#Create a function named prep_titanic that accepts the untransformed titanic data,
#and returns the data with the transformations above applied
def prep_titanic(df):
    df=df.pipe(titanic_missing_fill).pipe(titanic_remove_columns).pipe(encode_titanic)\
    .pipe(scale_titanic)
    return df

def prep_titanic_unscaled_age(df):
    df=df.pipe(titanic_missing_fill).pipe(titanic_remove_columns).pipe(encode_titanic)
    return df
    