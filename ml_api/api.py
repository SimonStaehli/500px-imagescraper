from transform import CustomTransformer
from model import CustomModel
from flask import Flask
from flask import request, jsonify
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
transformer = CustomTransformer()
model = CustomModel(filepath='model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Extract data from api
            data = request.get_json()
            data = pd.read_json(data)
            print('---- Received Data Object as JSON ----')
        except ValueError:
            return jsonify("Please enter a number.")
        # Data Transformation
        try:
            data = transformer.fit_transform(X=data)
            print('---- Transformed Data Successfully ----')
        except NotImplementedError:
            return jsonify('Something went wrong with the Transformation.')
        # Predictions
        try:
            predictions = model.model_predict(X=data)
            print('---- Data fed to the model and predictions returned ----')
        except NotImplementedError:
            return jsonify('Something went wrong with Predictions.')

        return jsonify(predictions.tolist())

@app.route('/score', methods=['POST'])
def get_model_score():
    if request.method == 'POST':
        try:
            data = request.get_json()
            X = pd.read_json(data['X']).to_numpy()
            y = pd.read_json(data['y']).to_numpy()
            print('---- Data Collected ----')
        except ValueError:
            return jsonify('No Valid Input for Model.')
        try:
            model_score = model.model_score(X=y, y=X)
            print('---- Data fed to model and Score returned ----')

        except TypeError:
            return jsonify('Datatype not valid. Be Sure to input list in format: [X, y]')

        return jsonify(model_score)

@app.route('/update_model', methods=['PUT'])
def update_model():
    if request.method == 'PUT':
        try:
            data = request.get_json()
            model_params = data['params']
            print('---- Data Collected ----')
        except ValueError:
            return jsonify('No Valid Input for Model.')
        try:
            model.update_model_params(new_params=model_params)
            print('---- Model updated with new parameters. ----')
        except TypeError:
            return jsonify('Parameters not accepted.')

        return jsonify('Parameters updated successfully.')

@app.route('/delete_model', methods=['DELETE'])
def delete_model():
    if request.method == 'DELETE':
        try:
            model.delete_model()
        except ValueError:
            return jsonify('No Valid Input for Model.')

        return jsonify('Model Deleted Successfully.')

@app.route('/model_params', methods=['GET'])
def model_parameters():
    if request.method == 'GET':
        try:
            model_params = model.return_parameters()
        except TypeError:
            return jsonify('Datatype not valid. Be Sure to input list in format: [X, y]')

        return jsonify(model_params.tolist())


if __name__ == '__main__':
    app.run(debug=True)