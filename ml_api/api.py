from transform import CustomTransformer
from model import CustomModel
from flask import Flask
from flask import request, jsonify
import numpy as np
import pandas as pd

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
        except:
            return jsonify('Something went wrong with the Transformation.')
        # Predictions
        try:
            predictions = model.model_predict(X=data)
            print('---- Data fed to the model and predictions returned ----')
        except:
            return jsonify('Something went wrong with Predictions.')

        return jsonify(predictions.tolist())

@app.route('/score', methods=['GET'])
def get_model_score():
    if request.method == 'GET':
        try:
            data = request.get_json()
        except:
            return jsonify('No Valid Input for Model.')
        try:
            model_score = model.model_score(X=data[0], y=data[1])
        except:
            return jsonify('Datatype not valid. Be Sure to input list in format: [X, y]')

        return model_score


@app.route('/model_params', methods=['GET'])
def score():
    if request.method == 'GET':
        try:
            model_params = model.return_parameters()
        except:
            return jsonify('Datatype not valid. Be Sure to input list in format: [X, y]')

        return model_params






if __name__ == '__main__':
    app.run(debug=True)