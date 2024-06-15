from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

class Predictor:
    def __init__(self, df):
        self.model = LinearRegression()
        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    

    def _fit_encoder(self, df, value='tipologia'):
        self.encoder.fit(df[[value]])

    def _transform_df(self, df, value='tipologia'):
        one_hot_encoded = self.encoder.transform(df[[value]])
        one_hot_encoded_df = pd.DataFrame(one_hot_encoded, columns=self.encoder.get_feature_names_out([value]))
        df = df.drop(value, axis=1)
        encoded = pd.concat([df, one_hot_encoded_df], axis=1)
        return encoded
    
    def fit(self, X, y):
        self._fit_encoder(X)
        X_encoded = self._transform_df(X)
        self.model.fit(X_encoded, y)
    
    def predict(self, X):
        X_encoded = self._transform_df(X)
        return self.model.predict(X_encoded)