from pprint import pprint
from math import sqrt

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
from pydataset import data
from statsmodels.formula.api import ols


def plot_residuals(x, y):
    '''
    Plots the residuals of a model that uses x to predict y. Note that we don't
    need to make any predictions ourselves here, seaborn will create the model
    and predictions for us under the hood with the `residplot` function.
    '''
    return sns.residplot(x, y)


def regression_errors(y, yhat):
    '''
    Returns a dictionary containing various regression error metrics.
    '''
    n = y.size
    residuals = yhat - y
    ybar = y.mean()

    sse = sum(residuals**2)

    ess = ((yhat - ybar)**2).sum()

    return {
        'sse': sse,
        'mse': sse / n,
        'rmse': sqrt(sse / n),
        'ess': ess,
        'tss': ess + sse,
    }


def baseline_mean_errors(y):
    '''
    Returns a dictionary containing various regression error metrics for a
    baseline model, that is, a model that uses the mean of y as the prediction.
    '''
    yhat = y.mean()
    n = y.size
    residuals = yhat - y

    sse = sum(residuals**2)

    return {
        'sse': sse,
        'mse': sse / n,
        'rmse': sqrt(sse / n),
    }


def better_than_baseline(y, yhat):
    '''
    Given the actual and predicted values, returns a boolean value indicating if
    the model's predictions are better than the baseline model.
    '''
    sse_baseline = baseline_mean_errors(y)['sse']
    sse_model = regression_errors(y, yhat)['sse']
    return sse_model < sse_baseline


def model_significance(model):
    '''
    Given a fitted OLS model from statsmodels, return the model's expanied
    variance, and the p-value indicating whether the relationship is
    significant.
    '''
    return {'r^2': model.rsquared, 'f p-value': model.f_pvalue}


if __name__ == '__main__':
    print('----> Loading tips data')
    tips = data('tips')

    print('----> Fitting OLS model')
    regr = ols('tip ~ total_bill', data=tips).fit()
    tips['yhat'] = regr.predict()

    print('----> Showing ressiduals for tip ~ total_bill')
    plot_residuals(tips.total_bill, tips.tip)
    plt.show()

    print('----> Error metrics for our model')
    pprint(regression_errors(tips.tip, tips.yhat))

    print('----> Baseline model error metrics')
    pprint(baseline_mean_errors(tips.total_bill))

    print('----> Is our model better than the baseline?')
    pprint(better_than_baseline(tips.total_bill, tips.yhat))

    print('----> Model significance metrics')
    regr = ols('tip ~ total_bill', tips).fit()
    pprint(model_significance(regr))
