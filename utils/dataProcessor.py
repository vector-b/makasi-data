import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler
class DataProcessor:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        self.scaler = MinMaxScaler()

    def _get_stats_by_key(self, key):
        budget = self.data_loader.dfs[key]['budget']
        return budget.describe()

    def _calculate_totals(self, key):
        budget = self.data_loader.dfs[key]['budget']
        total_material_cost = budget['Preço Material (Total)'].sum()
        total_execution_cost = budget['Preço Execução (Total)'].sum()
        total_cost = budget['Preço (Total)'].sum()
        
        return {
            'total_material_cost': total_material_cost,
            'total_execution_cost': total_execution_cost,
            'total_cost': total_cost
        }
    
    def _fit_encoder(self, df, value='tipologia'):
        self.encoder.fit(df[[value]])
        return self.encoder

    def _fit_scaler(self, df, numerical_columns):
        self.scaler.fit(df[numerical_columns])
        return self.scaler


    def _separate_numerical_categorical(self, df):
        numerical = df.select_dtypes(include=['float64', 'int64']).columns
        categorical = df.select_dtypes(include=['object']).columns
        return numerical, categorical
    
    def _transform_df(self, data,  scaler, encoder, use_scaler=True, value='tipologia'):

        df = data.copy()

        numerical, categorical = self._separate_numerical_categorical(df)
        if use_scaler:
            scaled = scaler.transform(df[numerical]) 
            scaled = pd.DataFrame(scaled, columns=numerical)
            df = df.drop(numerical, axis=1)

            df.reset_index(drop=True, inplace=True)
            scaled.reset_index(drop=True, inplace=True)

            scaled = pd.concat([df, scaled], axis=1)
        else:
            
            scaled = df

        one_hot_encoded = encoder.transform(scaled[[categorical[0]]])
        one_hot_encoded_df = pd.DataFrame(one_hot_encoded, columns=self.encoder.get_feature_names_out([value]))
        
        scaled.reset_index(drop=True, inplace=True)
        one_hot_encoded_df.reset_index(drop=True, inplace=True)

        scaled = scaled.drop(categorical[0], axis=1)

        encoded = pd.concat([scaled, one_hot_encoded_df], axis=1)

        return encoded
    
    def _encode_train_data(self, X, use_scaler=True):
        numerical, categorical = self._separate_numerical_categorical(X)

        scaler = self._fit_scaler(X, numerical)
        encoder = self._fit_encoder(X, categorical[0])
        
        X_encoded = self._transform_df(X, scaler, encoder)
        return X_encoded, scaler, encoder
    
    def _encode_test_data(self, X, scaler, encoder, use_scaler=True):
        X_encoded = self._transform_df(X, scaler, encoder)
        return X_encoded
    
    def aggregate_header_totals(self):
        headers = self.data_loader._compile_T_headers()
        total_costs = []
        total_material_costs = []
        total_execution_costs = []

        for _, header_row in headers.iterrows():
            budget_key = header_row['file']
            table_budget = self.data_loader.dfs[budget_key]['budget']

            total_cost = table_budget['Preço (Total)'].sum()

            total_material_cost = table_budget['Preço Material (Total)'].sum()
            total_execution_cost = table_budget['Preço Execução (Total)'].sum()


            total_costs.append(total_cost)
            total_material_costs.append(total_material_cost)
            total_execution_costs.append(total_execution_cost)
        
        headers['total_material_cost'] = total_material_costs
        headers['total_execution_cost'] = total_execution_costs
        headers['total_cost'] = total_costs

        headers.reset_index(drop=True, inplace=True)

        #self.headers_list = headers
        return headers
    
    def _concat_tables(self, headers):

        for _, header_row in headers.iterrows():
            budget_key = header_row['file']
            table_budget = self.data_loader.dfs[budget_key]['budget']
            table_t_header = self.data_loader.dfs[budget_key]['header_T']


            grouped_budget = self.data_loader._grouping_item_totals(table_budget)
            combined_data = pd.concat([table_t_header]*grouped_budget.shape[0], ignore_index=True)
            combined_data = pd.concat([grouped_budget, combined_data], axis=1)


            self.data_loader.dfs[budget_key]['combined'] = combined_data
        
        all_combined = pd.concat([self.data_loader.dfs[key]['combined'] for key in self.data_loader.dfs.keys()])
        #to_Print
        all_combined.reset_index(drop=True, inplace=True)
        #to_Print
        all_combined = all_combined.pivot_table(index=['file', 'titulo', 'tipologia', 'area_terreno', 'area_construída', 'area_fundação', 'area_fachada', 'area_parede', 'qtde_bwcs'],
                          columns='Descrição',
                          values='Preço (Total)',
                          aggfunc='sum').reset_index()
        
        return all_combined
