
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import pandas as pd
import numpy as np
import pickle

# @DatasetUrl: https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction
data = pd.read_csv('heart_failure_data.csv')

label_encoder = LabelEncoder()
data['ChestPainType'] = label_encoder.fit_transform(data['ChestPainType'])

label_encoder = LabelEncoder()
data['RestingECG'] = label_encoder.fit_transform(data['RestingECG'])

label_encoder = LabelEncoder()
data['ST_Slope'] = label_encoder.fit_transform(data['ExerciseAngina'])

label_encoder = LabelEncoder()
data['ExerciseAngina'] = label_encoder.fit_transform(data['ExerciseAngina'])

label_encoder = LabelEncoder()
data['Sex'] = label_encoder.fit_transform(data['Sex'])

columns = data.columns

X = data.iloc[:, :-1]
y = data.iloc[:, -1].astype(np.uint8)

scaler = StandardScaler()
scaler.fit(X)

X = scaler.transform(X)
X = pd.DataFrame(X, columns=columns[:-1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

clf = LogisticRegression()
clf.fit(X_train, y_train)

print("Train accuracy: ", clf.score(X_train, y_train))
print("Test accuracy:: ", clf.score(X_test, y_test))

preds = clf.predict(X_test)

print("Classification Report:")
print(classification_report(preds, y_test))

clf = SVC(probability=True)
clf.fit(X_train, y_train)

print("Train accuracy: ", clf.score(X_train, y_train))
print("Test accuracy:: ", clf.score(X_test, y_test))

preds = clf.predict(X_test)
# prob = clf.predict_proba(X_test)
print(preds)
# print(prob)

print("Classification Report:")
print(classification_report(preds, y_test))

print('Saving the trained model:')
with open('trained_model', 'wb') as model:
    pickle.dump(clf, model)

print('exit')

