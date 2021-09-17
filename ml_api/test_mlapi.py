from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_boston
import numpy as np
import pandas as pd
import requests
import pickle
import os
import pytest

# Note:
# Please make sure the api.py is running throughout the test
# otherwise the test will fail!

# Pre-Setup for test
test_digits = 6
X, y = load_boston(return_X_y=True)
model = LinearRegression()
model.fit(X, y)

# Save same model as pickle file
with open('model.pkl', 'wb') as model_file:
    pickle.dump(obj=model, file=model_file)

# Map Correct references for the model to check in tests
prediction_ref = model.predict(X)
score_ref = model.score(X, y)
coef_ref = model.coef_

del model

base_url = 'http://127.0.0.1:5000/'

############## Test Part ###############
data_X = pd.DataFrame(X)
data_X = data_X.to_json(orient='records')


def test_endpoint_con():
    """
    Function checks \check endpoint of the API
    """
    response = requests.get(url=base_url + '/check')

    assert response.json() == 200

def test_predict_endpoint():
    """
    Function checks \predict endpoint of the API
    """
    response = requests.post(url=base_url+'/predict', json=data_X)

    assert response.status_code == 200
    np.testing.assert_almost_equal(actual=np.array(response.json()), desired=prediction_ref,
                                   decimal=test_digits, verbose=True)

def test_score_endpoint():
    """
    Function checks \score endpoint of the API
    """
    data_y = pd.DataFrame(y)
    data_y = data_y.to_json(orient='records') # "records" bc pandas to_json() will mix up the index
    data_ = dict(X=data_X, y=data_y)

    response = requests.post(url=base_url+'/score', json=data_)
    assert response.status_code == 200
    assert round(response.json(), 6) == round(score_ref, 6)

def test_coef_endpoint():
    """
    Function checks \model_params endpoint of the API
    """
    response = requests.get(url=base_url + '/model_params')
    assert response.status_code == 200
    np.testing.assert_almost_equal(actual=np.array(response.json()), desired=coef_ref,
                                   decimal=test_digits, verbose=True)

def test_update_endpoint(coef_ref=coef_ref):
    """
    Function checks \update_model endpoint of the API
    """
    new_coef = np.random.uniform(size=len(coef_ref)).tolist()
    response = requests.put(url=base_url+'/update_model', json={'params': new_coef})
    assert response.status_code == 200

    with open('model.pkl', 'rb') as model_file:
        reference_model = pickle.load(model_file)
        coef_ref = reference_model.coef_

    np.testing.assert_array_almost_equal(x=coef_ref, y=new_coef,
                                        decimal=test_digits, verbose=True)

def test_delete_endpoint():
    """
    Function checks \delete_model endpoint of the API
    """
    response = requests.delete(url=base_url + '/delete_model')

    assert response.status_code == 200
    assert 'model.pkl' not in os.listdir()


if __name__ == '__main__':
    pytest.main()
