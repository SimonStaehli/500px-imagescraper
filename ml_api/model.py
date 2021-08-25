import numpy as np
import pandas as pd
import pickle
# Additional Imports
import sklearn


class CustomModel(object):
    """

    """

    def __init__(self, filepath):
        super(CustomModel, self).__init__()
        self.model = None
        self.filepath = filepath
        self._load_model()

    def _load_model(self):
        """

        Returns
        -------

        """
        with open(self.filepath, 'rb') as my_model:
            self.model = pickle.load(my_model)

    def model_predict(self, X):
        return self.model.predict(X=X)

    def model_score(self, X, y):
        return self.model.score(X, y)

