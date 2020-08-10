import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
import sklearn.metrics
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix



data = pd.read_csv('Sensor.csv')

describe = data.describe()
print(describe)

#print(data.head())

new_data = data.drop("Time", axis = 1)
print (new_data.head())

clf = KMeans(n_clusters = 5)
clf.fit(new_data)

centroids = clf.cluster_centers_
labels = clf.labels_

print(centroids)
print(labels)
print(len(labels))

print(new_data.columns)

new_data['clusters'] = labels

print(new_data)


new_set = new_data.to_csv("newset.csv")

newdata = pd.read_csv ("newset.csv", sep = ',', header=0)
#predictors = new_data[['Humidity %']]
predictors = newdata.values[:,0:3]

#predictors = new_data[Index(['Humidity %', 'Temperature degC', 'Temperature degF', 'Gas Conc.'], dtype='float')]
#target =newdata.clusters
target =newdata.values[:,5]
pred_train, pred_test, tar_train, tar_test = train_test_split(predictors, target, test_size = 0.3, random_state = 30)


classifier = DecisionTreeClassifier()
classifier = classifier.fit(pred_train, tar_train)

from sklearn.externals import joblib
joblib.dump(classifier, 'Gas sensor model')

joblib.load('Gas sensor model')



prediction = classifier.predict(pred_test)

#print(classifier)
print("Level Predictions: ", prediction)
#print (tar_test)

print("Confusion Matrix: ", sklearn.metrics.confusion_matrix(tar_test, prediction))
print("Model Accuracy: ", sklearn.metrics.accuracy_score(tar_test, prediction))