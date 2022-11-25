
from flask import Flask, redirect, url_for, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import pickle

# @DatasetUrl: https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction
df = pd.read_csv('heart_failure_data.csv')

label_encoder = LabelEncoder()
df['ChestPainType'] = label_encoder.fit_transform(df['ChestPainType'])

label_encoder = LabelEncoder()
df['RestingECG'] = label_encoder.fit_transform(df['RestingECG'])

label_encoder = LabelEncoder()
df['ST_Slope'] = label_encoder.fit_transform(df['ExerciseAngina'])

label_encoder = LabelEncoder()
df['ExerciseAngina'] = label_encoder.fit_transform(df['ExerciseAngina'])

label_encoder = LabelEncoder()
df['Sex'] = label_encoder.fit_transform(df['Sex'])

columns = df.columns

X = df.iloc[:, :-1]

scaler = StandardScaler()
scaler.fit(X)

app = Flask(__name__)

trained_model = None

with open('trained_model', 'rb') as f:
    trained_model = pickle.load(f)

@app.route('/infer', methods=['POST'])
def infer():

    if not trained_model:
        resp = jsonify({
            'status': False,
            'message': 'Unable to load the model. Please contact the owner of this endpoint.'
        })

        resp.headers.add('Access-Control-Allow-Origin', '*')

        return resp

    request_data = {}
    values = request.form.values()
    values = list(values)

    columns = [
        'Age',
        'Sex',
        'ChestPainType',
        'RestingBP',
        'Cholesterol',
        'FastingBS',
        'RestingECG',
        'MaxHR',
        'ExerciseAngina',
        'Oldpeak',
        'ST_Slope'
    ]

    for i in range(len(values)):
        if columns[i] not in request_data:
            request_data[columns[i]] = []

        request_data[columns[i]].append(float(values[i]))

    data = pd.DataFrame.from_dict(request_data)

    data = scaler.transform(data)
    data = pd.DataFrame(data, columns=columns)

    prediction = trained_model.predict_proba(data)
    label, prob = np.argmax(prediction[0]), np.max(prediction[0])

    has_heart_disease = True if label == 1 else False

    resp = jsonify({
        'status': True,
        'has_heart_disease': has_heart_disease,
        'probability': float(prob)
    })

    resp.headers.add('Access-Control-Allow-Origin', '*')

    return resp


@app.route('/')
def home():
    return {'message': 'Welcome to the Cloud Computing project by Neha zareen, Mohammed Abdul Ghani, and Kowshiq Babu Indupuri'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


