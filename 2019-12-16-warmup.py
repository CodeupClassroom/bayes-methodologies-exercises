# IPython log file


from pydataset import data
df = data('voteincome')
data('voteincome', show_doc=True)
df
df = df.drop(columns=['state', 'year'])
from sklearn.model_selection import train_test_split
df
X = df.drop(columns='vote')
y = df.vote
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=4)
knn.fit(X_train, y_train)
knn.score(X_train, y_train)
knn.score(X_test, y_test)
from sklearn.metrics import accuracy_score
accuracy_score(y_train, knn.predict(X_train))
for n in [1, 2, 3, 4]:
    knn = KNeighborsClassifier(n_neighbors=n)
    knn.fit(X_train, y_train)
    print('-------')
    print('n:', n)
    print('train score:', knn.score(X_train, y_train))
    print('test score:', knn.score(X_test, y_test))
    
knn = KNeighborsClassifier(n_neighbors=1).fit(X_train, y_train)
training_predictions = knn.predict(X_train, y_train)
training_predictions = knn.predict(X_train)
test_predictions = knn.predict(X_test)
from sklearn.metrics import classification_report
X
classification_report(y_train, training_predictions)
print(classification_report(y_train, training_predictions))
from sklearn import __version__
__version__
def test_score(n_neighbors):
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X_train, y_train)
    return model.score(X_test, y_test)
    
test_score(3)
{n: test_score(n) for n in range(1, 21)}
pd.Series({n: test_score(n) for n in range(1, 21)})
import pandas as pd
pd.Series({n: test_score(n) for n in range(1, 21)})
pd.Series({n: test_score(n) for n in range(1, 21)}, name='test accuracy')
pd.Series({n: test_score(n) for n in range(1, 21)}, name='test accuracy').plot()
import matplotlib.pyplot as plt
plt.show()
pd.Series({n: test_score(n) for n in range(1, 21)}, name='test accuracy').plot()
plt.xticks(range(1, 21))
plt.ylabel('Accuracy')
plt.xlabel('n_neighbors')
plt.title('Accuracy on test data v n neighbors')
plt.show()
