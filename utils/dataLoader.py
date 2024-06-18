import pandas as pd
import pydoc

class DataLoader:
    """
        This class is responsible for loading the data from the csv files and pre-processing the data
        Including reading csv files, processing the header and the budget table, Transposing tables, grouping values and renaming columns
    """
    def __init__(self) -> None:
        """
            Function to initialize the DataLoader object
            This class is responsible for loading the data from the csv files and pre-processing the data

            Sets the dfs attribute as an empty dictionary - it will store the data from the csv files
        """
        self.dfs = {}

    def get_filepath(self, data_dir, file_name) -> str:
        """
            Function to get the file path
            Args:
                data_dir: str
                file_name: str
            Returns:
                str
        """
        return f"{data_dir}/{file_name}"

    def convert_money_columns_to_float(self, df, columns) -> pd.DataFrame:
        """
            Function to convert columns with money values to float
            Args:
                df: pandas DataFrame
                columns: list
            Returns:
                pandas DataFrame
        """
        for col in columns:
            df[col] = df[col].apply(lambda x: float(x.replace('R$', '').replace('.', '').replace(',', '.')) if isinstance(x, str) else x)
        return df

    def convert_values_to_float(self, df, columns) -> pd.DataFrame:
        """
            Function to convert string values to float, like '1.000,00' to 1000.00
            Args:
                df: pandas DataFrame
                columns: list
            Returns:
                pandas DataFrame
        """
        for col in columns:
            try:
                df[col] = df[col].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) else x)
            except:
                pass
        return df
    
    def rename_columns(self, df) -> pd.DataFrame:
        """
            Function to rename the columns of the DataFrame
            Removes spaces, accents and special characters
            Args:
                df: pandas DataFrame
            Returns:
                pandas DataFrame
        """
        df.columns = [col.lower().replace(' ', '_').replace('á', 'a').replace('`', '') for col in df.columns]
        return df


    def process_header(self, path, file_name) -> tuple:
        """
            Function to process the header of the csv file
            This function reads the first 9 lines of the file and returns the header DataFrame
            It also return the Transposed DataFrame of the header
    
            Args:
                path: str
                file_name: str

            Returns:
                tuple
        """
            

        header = pd.read_csv(path, skiprows=1, nrows=8, header=None)
        header = header.iloc[:, :2]
        header.columns = ['Info', 'Valor']
        header = header.dropna(subset=['Info', 'Valor'])
        header = header[['Info', 'Valor']]

        header_T = header.set_index('Info').T

        float_cols = ['Área Terreno', 'Área Construída', 'Área Fundação', 'Área Fachada', 'Área Parede', 'Qtde BWCs']
        header_T = self.convert_values_to_float(header_T, float_cols)
        header_T.insert(0, 'File', file_name.replace('.csv', ''))
        #header_T['Área Construída por BWC'] = header_T['Área Construída'] / header_T['Qtde BWCs']
        header_T = self.rename_columns(header_T)
        #create a new column that is an operation of two columns (Área Construída / Qtde BWCs)
        

        header_T.reset_index(drop=True, inplace=True)


        return header, header_T


    def grouping_item_totals(self, data):
        """
            Function to group the budget table by the first part of the Item column
            It will sum the values of the columns: Preço Material (Total), Preço Execução (Total) and Preço (Total)
            Args:
                data: pandas DataFrame
            Returns:
                pandas DataFrame
        """
        df = data.copy()
        df['Categoria'] = df['Item'].apply(lambda x: x.split('.')[0])
        df['Item'] = df['Item'].str.replace('.', '')
        df['Item'] = df['Item'].astype(int)

        df_grouped = df.groupby('Categoria').agg({
            'Item': 'first',
            'Descrição': 'first',
            'Preço Material (Total)' : 'sum',
            'Preço Execução (Total)': 'sum',
            'Preço (Total)': 'sum'
        }).reset_index(drop=True)

        df_grouped.sort_values('Item', inplace=True)
        df_grouped.set_index('Item', inplace=True)

        return df_grouped
        

    def load_data_from_path(self, data_dir, file_names):
        """
            Function to load the data from the csv files
            It will process the header using process_header function 
            and the budget table using pd.read_csv ignoring the first 11 lines
            Append the data to the self.dfs dictionary
            Args:
                data_dir: str
                file_names: list

            Returns:
                None
        """

        for name in file_names:
            path = self.get_filepath(data_dir, name)
            '''Leitor de Header - Primeiras 9 linhas'''
            header, header_T = self.process_header(path, name)

            '''Caso de MultiIndex:
                Preço Material - Preço Execução - Preço
                Unitário - Total
            '''
            df = pd.read_csv(path, skiprows=11, header=[0, 1], delimiter=',', skipinitialspace=True)
            
            '''
                Manualmente definindo o nome das colunas MultiIndex
                =)
            '''
            df.columns = ['Item', 'Referência', 'Tipo', 'Código', 'Descrição', 'Unid.', 'Quantidade', 'BDI', 
              'Preço Material (Unitário)', 'Preço Material (Total)', 'Preço Execução (Unitário)', 
              'Preço Execução (Total)', 'Preço (Unitário)', 'Preço (Total)']

            price_columns = [col for col in df.columns if 'Preço' in col]
            df = self.convert_money_columns_to_float(df, price_columns)

            key_name = name.replace('.csv', '')
            self.dfs[key_name] = {
                'header': header,
                'header_T': header_T,
                'budget': df
            }
    
    def load_predict_set(self, data_dir, file_name):
        """
            Function to load the predict set
            It will process the header using process_header function
            Args:
                data_dir: str
                file_name: str

            Returns:
                tuple
        """
        path = self.get_filepath(data_dir, file_name)
        header, header_T = self.process_header(path, file_name)

        self.predict_df = header_T
        return header, header_T
        
    def compile_T_headers(self):
        """
            Function to compile the Transposed headers
            It will return a DataFrame with all the headers
            Args:
                None
            Returns:
                pandas DataFrame
        """
        headers = []
        for key in self.dfs:
            headers.append(self.dfs[key]['header_T'])
        return pd.concat(headers)
    
