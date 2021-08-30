import numpy as np
import pandas as pd
import pickle
import os
# Additional Imports
import sklearn


class CustomModel(object):
    """
    Model Class for the ML-API
    """

    def __init__(self, filepath):
        """

        Parameters
        ----------
        filepath:
            Path to your model. Preferably in pickle format.

        """
        super(CustomModel, self).__init__()
        self.model = None
        self.filepath = filepath
        self._load_model()

    def _load_model(self):
        """
        This function is called at initialization of the class and loads
        model as attribute to class
        """
        with open(self.filepath, 'rb') as my_model:
            self.model = pickle.load(my_model)

    def model_predict(self, X):
        """
        Returns predictions of the model to given X.

        Parameters
        ----------
        X:
            Data as numpy array or compatible with model.

        Returns
        -------
        y_pred:
            predictions according to X

        """
        return self.model.predict(X=X)

    def model_score(self, X, y):
        """
        Returns the score of the model for given data.
        This method is strongly related to the class of the model and which attributes it provides.

        Parameters
        ----------
        X:
            Predictor variables
        y:
            Target variable

        Returns
        -------
        score:
            score according to model description (mostly R2 or Accuracy)

        """
        return self.model.score(X, y)

    def return_parameters(self):
        """
        THis method is strongly related to the class attributes of the model.
        i.E. LinearRegression class does not have same attributes as KNN class.

        Returns
        -------
        model_coef:
            Coefficients of the model.

        """
        try:
            model_coef = self.model.coef_
        except:
            model_coef = 'Model does not have a .coef_ attribute.'

        return model_coef

    def delete_model(self):
        """
        Deletes the model in given filepath object.

        Returns
        -------
        None
        """
        os.remove(self.filepath)
        self.model = None

    def update_model_params(self, new_params):
        """
        Replaces the old parameters of the model by new parameters.
        This method is strongly related to the class object and needs to be adapted in advance.

        Returns
        -------
        None
        """
        new_params = np.array(new_params)
        self.model.coef_ = new_params


