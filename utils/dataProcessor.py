import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler
class DataProcessor:
    """
        This class is responsible for processing the data and preparing it for the model and for further analysis
        It diverges from the DataLoader class, which is responsible for loading the data from the csv files
        Here, we will process the data, calculate statistics and prepare the data for the model

    """
    def __init__(self, data_loader):
        """
            Function to initialize the DataProcessor object

            Initial variables:
                data_loader: DataLoader object - it will be used to access the data previously loaded
                encoder: OneHotEncoder object
                scaler: MinMaxScaler object

            Args:
                data_loader: DataLoader object

        """
        self.data_loader = data_loader
        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        self.scaler = MinMaxScaler()

    def get_stats_by_key(self, key) -> pd.DataFrame:
        """
            Function to get the statistics of the budget dataframe (second table) given a key

            Args:
                key: str

            Returns:
        """
        budget = self.data_loader.dfs[key]['budget']
        return budget.describe()

    def calculate_totals(self, key) -> dict:
        """
            Function to calculate the total costs of the budget dataframe,
            It gets the sum of the 'Preço Material (Total)', 'Preço Execução (Total)' and 'Preço (Total)' columns
            and returns a dictionary with the results

            Args:

                key: str

            Returns:
                dict

        """
        budget = self.data_loader.dfs[key]['budget']
        total_material_cost = budget['Preço Material (Total)'].sum()
        total_execution_cost = budget['Preço Execução (Total)'].sum()
        total_cost = budget['Preço (Total)'].sum()
        
        return {
            'total_material_cost': total_material_cost,
            'total_execution_cost': total_execution_cost,
            'total_cost': total_cost
        }
    
    def fit_encoder(self, df, value='tipologia') -> OneHotEncoder:
        """
            Function to fit the OneHotEncoder

            Args:
                df: pandas DataFrame
                value: str

            Returns:
                OneHotEncoder object
        """
        self.encoder.fit(df[[value]])
        return self.encoder

    def fit_scaler(self, df, numerical_columns) -> MinMaxScaler:
        """
            Function to fit the MinMaxScaler

            Args:
                df: pandas DataFrame
                numerical_columns: list

            Returns:
                MinMaxScaler object
        """
        self.scaler.fit(df[numerical_columns])
        return self.scaler


    def separate_numerical_categorical(self, df) -> tuple:
        """
            Function to separate the numerical and categorical columns of a DataFrame

            Args:
                df: pandas DataFrame

            Returns:
                tuple
        """
        numerical = df.select_dtypes(include=['float64', 'int64']).columns
        categorical = df.select_dtypes(include=['object']).columns
        return numerical, categorical
    
    def transform_df(self, data,  scaler, encoder, value='tipologia') -> pd.DataFrame:
        """
            Function to transform the DataFrame using the fitted MinMaxScaler and OneHotEncoder

            Args:
                data: pandas DataFrame
                scaler: MinMaxScaler object
                encoder: OneHotEncoder object
                value: str

            Returns:
                pandas DataFrame
        """

        df = data.copy()

        numerical, categorical = self.separate_numerical_categorical(df)
        
        scaled = scaler.transform(df[numerical]) 
        scaled = pd.DataFrame(scaled, columns=numerical)
        df = df.drop(numerical, axis=1)

        df.reset_index(drop=True, inplace=True)
        scaled.reset_index(drop=True, inplace=True)

        scaled = pd.concat([df, scaled], axis=1)
    

        one_hot_encoded = encoder.transform(scaled[[categorical[0]]])
        one_hot_encoded_df = pd.DataFrame(one_hot_encoded, columns=self.encoder.get_feature_names_out([value]))
        
        scaled.reset_index(drop=True, inplace=True)
        one_hot_encoded_df.reset_index(drop=True, inplace=True)

        scaled = scaled.drop(categorical[0], axis=1)

        encoded = pd.concat([scaled, one_hot_encoded_df], axis=1)

        return encoded
    
    def encode_train_data(self, X) -> tuple:
        """
            Function to separate the numerical and categorical columns of a DataFrame and fit the MinMaxScaler and OneHotEncoder

            Args:
                X: pandas DataFrame

            Returns:
                tuple            
        """
        numerical, categorical = self.separate_numerical_categorical(X)

        scaler = self.fit_scaler(X, numerical)
        encoder = self.fit_encoder(X, categorical[0])
        
        X_encoded = self.transform_df(X, scaler, encoder)
        return X_encoded, scaler, encoder
    
    def encode_test_data(self, X, scaler, encoder) -> pd.DataFrame:
        """
            Function to transform the DataFrame using the previously fitted MinMaxScaler and OneHotEncoder

            Args:
                X: pandas DataFrame
                scaler: MinMaxScaler object
                encoder: OneHotEncoder object
            
            Returns:
                pandas DataFrame
        """

        X_encoded = self.transform_df(X, scaler, encoder)
        return X_encoded
    
    def aggregate_header_totals(self) -> pd.DataFrame:
        """
            Function to aggregate the total costs of the budget tables

            Args:
                None
            
            Returns:
                pandas DataFrame
        """
        headers = self.data_loader.compile_T_headers()
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
    
    def concat_tables(self, headers):
        """
            Function to concatenate the budget tables with the header tables
            For each header, it will concatenate the budget table with the transposed header table from headers

            Args:
                headers: pandas DataFrame
            
            Returns:
                pandas DataFrame
        """

        for _, header_row in headers.iterrows():
            budget_key = header_row['file']
            table_budget = self.data_loader.dfs[budget_key]['budget']
            table_t_header = self.data_loader.dfs[budget_key]['header_T']


            grouped_budget = self.data_loader.grouping_item_totals(table_budget)
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
    