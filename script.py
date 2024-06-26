import pandas as pd
import seaborn as sns
from utils.dataLoader import DataLoader
from utils.dataProcessor import DataProcessor
from utils.models import Predictor


#Initializating the DataLoader
loader = DataLoader()

#Reading Files
datadir = 'src/datasets'
files = ['amostra_projeto1.csv', 'amostra_projeto_2.csv', 'amostra_projeto_3.csv']

loader.load_data_from_path(datadir, files)
loader.load_predict_set(datadir, 'projeto_4.csv')

#Initializating the DataProcessor
processor = DataProcessor(loader)

#Agggregating the header totals
h_totals = processor.aggregate_header_totals()

header_totals = h_totals.copy()

#Choosing the columns to predict
totals = ['total_execution_cost','total_material_cost','total_cost']

#Initializing the Predictor
prd = Predictor(header_totals)

#Choosing the features to train the model
train_cols = [col for col in header_totals.columns if col not in ['file', 'titulo', 'area_fundação', 'total_cost', 'total_execution_cost', 'total_material_cost']]

#Splitting the data into X and y
X = header_totals[train_cols]
y = header_totals['total_cost']

#Encoding the X data
X, scaler, encoder  = processor.encode_train_data(X)

#Fitting the model
prd.fit(X,y)

#Predict
pred = prd.predict(X)

print('Avaliando com conjunto de treino:')
#Getting metrics
prd.get_metrics(y, pred)


#------------------------------------------ TEST SET ------------------------------------------#
#Splitting the data - 2 samples for training and 1 for testing
X_train, X_test, y_train, y_test = X.iloc[:2], X.iloc[2:], y.iloc[:2], y.iloc[2:]

#Fitting the model
prd.fit(X_train, y_train)

#Predict
pred = prd.predict(X_test)

print('Avaliando com conjunto de teste:')
#Getting metrics
prd.get_metrics(y_test, pred)

