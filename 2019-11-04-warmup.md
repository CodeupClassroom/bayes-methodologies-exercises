# Regression Modeling Warmup

1. Using `pydataset`, load the `faithful` dataset and read it's documentation.

1. What is pearson's r for the two variables?

1. Visualize the relationship between the variables.

1. Build a linear model that predicts `eruptions` based on `waiting`.

1. Create a visualization with your predictions

    1. `waiting` should be on the x axis, and `eruptions` on the y
    1. Use color to differentiate the actual vs predicted values.
    1. Add a descriptive title.
    1. Change the y ticks such that they are all integers (i.e. no decimals)
    1. Add the root mean squared error of your predictions as an annotation

```python
from pydataset import data

faithful = data('faithful')
faithful
```

```python
faithful.corr()
```

```python
%matplotlib inline
import matplotlib.pyplot as plt

faithful.plot.scatter(y='eruptions', x='waiting')
```

```python
from sklearn.linear_model import LinearRegression
```

```python
X, y = faithful[['waiting']], faithful['eruptions']

# X is a dataframe
# y is a series
```

```python
model = LinearRegression().fit(X, y)
model
```

```python
from math import sqrt
from sklearn.metrics import mean_squared_error

predictions = model.predict(X)

rmse = sqrt(mean_squared_error(y, predictions))

plt.figure(figsize=(14, 8))
plt.scatter(X, y, label='Actual Value', alpha=.6)
plt.scatter(X, predictions, label='Prediction', alpha=.6)
plt.xlabel('Waiting (minutes)')
plt.ylabel('Eruptions (minutes)')
plt.title('Actual vs Predicted Eruptions')
plt.legend()
plt.yticks(range(0, 7))
plt.text(50, 5, f'RMSE: {rmse:.4f}', size=16)
```

```python
faithful['yhat'] = predictions
faithful = faithful[['waiting', 'eruptions', 'yhat']]
faithful
```

```python
melt = faithful.melt(id_vars=['waiting'])
melt
```

```python
import seaborn as sns

sns.relplot(data=melt, x='waiting', y='value', hue='variable')
```
