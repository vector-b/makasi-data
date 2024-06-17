import pandas as pd
import seaborn as sns
from utils.dataLoader import DataLoader
from utils.dataProcessor import DataProcessor
from utils.models import Predictor


loader = DataLoader()

datadir = 'src/datasets'
files = ['amostra_projeto1.csv', 'amostra_projeto_2.csv', 'amostra_projeto_3.csv']

loader._load_data_from_path(datadir, files)
loader._load_predict_set(datadir, 'projeto_4.csv')


processor = DataProcessor(loader)
h_totals = processor.aggregate_header_totals()

header_totals = h_totals.copy()
totals = ['total_execution_cost','total_material_cost','total_cost']

prd = Predictor(header_totals)
train_cols = [col for col in header_totals.columns if col not in ['file', 'titulo', 'area_fundação', 'total_cost', 'total_execution_cost', 'total_material_cost']]
X = header_totals[train_cols]
y = header_totals['total_cost']

X, scaler, encoder  = processor._encode_train_data(X)

prd.fit(X,y)
pred = prd.predict(X)


#------------------------------------------ TEST SET ------------------------------------------#
X_train, X_test, y_train, y_test = X.iloc[:2], X.iloc[2:], y.iloc[:2], y.iloc[2:]
prd.fit(X_train, y_train)
pred = prd.predict(X_test)

prd._get_metrics(y_test, pred)

