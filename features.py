from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
import pandas as pd
import numpy as np


def optimal_number_of_features(X_train, y_train, X_test, y_test):
    '''discover the optimal number of featuresm, n, using our scaled x and y dataframes, recursive feature
    elimination and linear regression (to test the performance with each number of features).
    We will use the output of this function (the number of features) as input to the next function
    optimal_features, which will then run recursive feature elimination to find the n best features'''

    number_of_attributes = X_train.shape[1]
    number_of_features_list=np.arange(1,number_of_attributes)
    high_score=0
    
    #Variable to store the optimum features
    number_of_features=0           
    score_list =[]
    
    for n in range(len(number_of_features_list)):
        model = LinearRegression()
        rfe = RFE(model,number_of_features_list[n])
        X_train_rfe = rfe.fit_transform(X_train,y_train)
        X_test_rfe = rfe.transform(X_test)
        model.fit(X_train_rfe,y_train)
        score = model.score(X_test_rfe,y_test)
        score_list.append(score)
        if(score>high_score):
            high_score = score
            number_of_features = number_of_features_list[n]
    return number_of_features

def optimal_features(X_train, y_train, number_of_features):
    '''Taking the output of optimal_number_of_features, as n, and use that value to 
    run recursive feature elimination to find the n best features'''
    cols = list(X_train.columns)
    model = LinearRegression()
    
    #Initializing RFE model
    rfe = RFE(model, number_of_features)

    #Transforming data using RFE
    X_rfe = rfe.fit_transform(X_train,y_train)  

    #Fitting the data to model
    model.fit(X_rfe,y_train)
    temp = pd.Series(rfe.support_,index = cols)
    selected_features_rfe = temp[temp==True].index
    
    return selected_features_rfe