from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, root_mean_squared_error
import statsmodels.api as sm
import pandas as pd


class Predictor:
    def __init__(self, df):
        self.model = LinearRegression()
        self.stats_model = sm.OLS

    def fit(self, X, y):
        self.model.fit(X, y)
    
    def fit_stats_model(self, X, y):
        X = sm.add_constant(X)
        self.stats_model = self.stats_model(y, X)
        self.stats_model = self.stats_model.fit()
        print(self.stats_model.summary())
    
    def predict(self, X):
        return self.model.predict(X)
    
    def _get_metrics(self, y, pred):
        #print metrics rounded to 2 decimal places
        print(f'MSE: {round(mean_squared_error(y, pred), 2)}')
        print(f'MAE: {round(mean_absolute_error(y, pred), 2)}')
        print(f'RMSE: {round(root_mean_squared_error(y, pred), 2)}')

        
