from sklearn.feature_selection import SelectKBest, f_regression, RFE
import statsmodels.api as sm
from sklearn.linear_model import LassoCV, LinearRegression


def select_kbest_freg_unscaled(X_train, y_train, k):
    '''
    Takes unscaled data (X_train, y_train) and number of features to select (k) as input
    and returns a list of the top k features
    '''
    f_selector = SelectKBest(f_regression, k).fit(X_train, y_train).get_support()
    f_feature = X_train.loc[:,f_selector].columns.tolist()
    return f_feature

def select_kbest_freg_scaled(X_train, y_train, k):
    '''
    Takes unscaled data (X_train, y_train) and number of features to select (k) as input
    and returns a list of the top k features
    '''
    f_selector = SelectKBest(f_regression, k).fit(X_train, y_train).get_support()
    f_feature = X_train.loc[:,f_selector].columns.tolist()
    return f_feature

def select_kbest_freg(X, y, k):
    '''
    dataframe of features (X),  dataframe of the target (y), and number of features to select (k) as input
    and returns a list of the top k features
    '''
    f_selector = SelectKBest(f_regression, k).fit(X, y).get_support()
    f_feature = X.loc[:,f_selector].columns.tolist()
    return f_feature

def ols_backward_elimination(X_train, y_train):
    '''
    Takes dataframe of features and dataframe of target variable as input,
    runs OLS, extracts each features p-value, removes the column with the highest p-value
    until there are no features remaining with a p-value > 0.05
    It then returns a list of the names of the selected features
    '''
    cols = list(X_train.columns)

    while (len(cols) > 0):
        # create a new dataframe that we will use to train the model...each time we loop through it will 
        # remove the feature with the highest p-value IF that p-value is greater than 0.05.
        # if there are no p-values > 0.05, then it will only go through the loop one time. 
        X_1 = X_train[cols]
        # fit the Ordinary Least Squares Model
        model = sm.OLS(y_train,X_1).fit()
        # create a series of the pvalues with index as the feature names
        p = pd.Series(model.pvalues)
        # get the max p-value
        pmax = max(p)
        # get the feature that has the max p-value
        feature_with_p_max = p.idxmax()
        # if the max p-value is >0.05, the remove the feature and go back to the start of the loop
        # else break the loop with the column names of all features with a p-value <= 0.05
        if(pmax>0.05):
            cols.remove(feature_with_p_max)
        else:
            break

    selected_features_BE = cols
    return selected_features_BE


    def optimal_number_of_features(X, y):
    '''discover the optimal number of features, n, using our scaled x and y dataframes, recursive feature
    elimination and linear regression (to test the performance with each number of features).
    We will use the output of this function (the number of features) as input to the next function
    optimal_features, which will then run recursive feature elimination to find the n best features
    '''
    features_range = range(1, len(X.columns)+1)
    # len(features_range)

    # set "high score" to be the lowest possible score
    high_score = 0

    # variables to store the feature list and number of features
    number_of_features = 0
    # score_list = []

    # write the problem without a loop, but instead with all features available,
    # so feature count = len(X_train_scaled.columns)
    for n in features_range:
        model = LinearRegression()
        train_rfe = RFE(model, n).fit_transform(X, y)
        model.fit(train_rfe, y)
        score = model.score(train_rfe, y)
        # score_list.append(score)
        if(score > high_score):
            high_score = score
            number_of_features = n

    return number_of_features, score

def optimal_features(X_train, X_test, y_train, number_of_features):
    '''Taking the output of optimal_number_of_features, as n, and use that value to 
    run recursive feature elimination to find the n best features'''
    cols = list(X_train.columns)
    model = LinearRegression()
    
    #Initializing RFE model
    rfe = RFE(model, number_of_features)

    #Transforming data using RFE
    train_rfe = rfe.fit_transform(X_train,y_train)
    test_rfe = rfe.transform(X_test)
    
    #Fitting the data to model
    model.fit(train_rfe, y_train)
    temp = pd.Series(rfe.support_,index = cols)
    selected_features_rfe = temp[temp==True].index
    
    X_train_rfe = pd.DataFrame(train_rfe, columns=selected_features_rfe)
    X_test_rfe = pd.DataFrame(test_rfe, columns=selected_features_rfe)
    
    return selected_features_rfe, X_train_rfe, X_test_rfe
