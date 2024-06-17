from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler, StandardScaler

import statsmodels.api as sm
import pandas as pd

class Predictor:
    def __init__(self, df):
        self.model = LinearRegression()
        self.stats_model = sm.OLS
        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        self.scaler = MinMaxScaler()

    def _fit_encoder(self, df, value='tipologia'):
        self.encoder.fit(df[[value]])

    def _fit_scaler(self, df, numerical_columns):
        self.scaler.fit(df[numerical_columns])

    def _separate_numerical_categorical(self, df):
        numerical = df.select_dtypes(include=['float64', 'int64']).columns
        categorical = df.select_dtypes(include=['object']).columns
        return numerical, categorical
    
    def _transform_df(self, data, use_scaler=True, value='tipologia'):
        df = data.copy()
        numerical, categorical = self._separate_numerical_categorical(df)
        if use_scaler:
            scaled = self.scaler.transform(df[numerical]) 
            scaled = pd.DataFrame(scaled, columns=numerical)
            df = df.drop(numerical, axis=1)
            scaled = pd.concat([df, scaled], axis=1)
        else:
            
            scaled = df

        one_hot_encoded = self.encoder.transform(scaled[[categorical[0]]])
        one_hot_encoded_df = pd.DataFrame(one_hot_encoded, columns=self.encoder.get_feature_names_out([value]))
        
        scaled.reset_index(drop=True, inplace=True)
        one_hot_encoded_df.reset_index(drop=True, inplace=True)

        scaled = scaled.drop(categorical[0], axis=1)
 
        encoded = pd.concat([scaled, one_hot_encoded_df], axis=1)

        return encoded
    
    def fit(self, X, y, use_scaler=True):
        numerical, categorical = self._separate_numerical_categorical(X)

        self._fit_scaler(X, numerical)
        self._fit_encoder(X, categorical[0])
        
        X_encoded = self._transform_df(X, use_scaler)
        print(X_encoded)
        self.model.fit(X_encoded, y)
    
    def fit_stats_model(self, X, y):
        self._fit_encoder(X)
        X_encoded = self._transform_df(X)
        X_encoded = sm.add_constant(X_encoded)
        self.stats_model = self.stats_model(y, X_encoded)
        self.stats_model = self.stats_model.fit()
        print(self.stats_model.summary())
    
    def predict(self, X, use_scaler=True):
        X_encoded = self._transform_df(X, use_scaler)
        return self.model.predict(X_encoded)