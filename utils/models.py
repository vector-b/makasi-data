import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, root_mean_squared_error
import statsmodels.api as sm
import pandas as pd


class Predictor:
    """
        This class is responsible for fitting the model and making predictions
        The functions here are quite simple, but they can be expanded to include more complex models and methods

    """
    def __init__(self, df):
        """
            Function to initialize the predictor object

            Initial variables:
                model: LinearRegression object
                stats_model: OLS object

            Args:
                df: pandas DataFrame

        """
        self.model = LinearRegression()
        self.stats_model = sm.OLS

    def fit(self, X, y) -> None:
        """
            Function to fit the Machine Learning model
            By default, it uses a Linear Regression model

            Args:
                X: pandas DataFrame
                y: pandas Series
        """
        self.model.fit(X, y)
    
    def fit_stats_model(self, X, y) -> None:
        """
            Function to fit the stats model
            By default, it uses an OLS model

            Args:
                X: pandas DataFrame
                y: pandas Series
        """
        X = sm.add_constant(X)
        self.stats_model = self.stats_model(y, X)
        self.stats_model = self.stats_model.fit()
        print(self.stats_model.summary())
    
    def predict(self, X) -> np.array:
        """
            Function to predict the target variable

            Args:
                X: pandas DataFrame

            Returns:
                numpy array
        """
        return self.model.predict(X)
    
    def get_metrics(self, y, pred) -> None:
        """
            Function to get the metrics of the model

            Args:
                y: pandas Series
                pred: numpy array
        """
        print(f'MSE: {round(mean_squared_error(y, pred), 2)}')
        print(f'MAE: {round(mean_absolute_error(y, pred), 2)}')
        print(f'RMSE: {round(root_mean_squared_error(y, pred), 2)}')

        