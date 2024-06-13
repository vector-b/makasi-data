import pandas as pd

class DataLoader:
    def __init__(self):
        self.dfs = {}

    def _get_filepath(self, data_dir, file_name):
        return f"{data_dir}/{file_name}"

    def _convert_money_columns_to_float(self, df, columns):
        for col in columns:
            df[col] = df[col].apply(lambda x: float(x.replace('R$', '').replace('.', '').replace(',', '.')) if isinstance(x, str) else x)
        return df

    def _convert_values_to_float(self, df, columns):
        #first replace , by . and then convert to float
        for col in columns:
            try:
                df[col] = df[col].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) else x)
            except:
                pass
        return df
    
    def _load_data_from_path(self, data_dir, file_names):
        for name in file_names:
            path = self._get_filepath(data_dir, name)
            '''Leitor de Header - Primeiras 9 linhas'''
            header = pd.read_csv(path,skiprows=1, nrows=8, header=None)

            header = header.iloc[:, :2]
            header.columns = ['Info', 'Valor']
            header = header.dropna(subset=['Info', 'Valor'])
            header = header[['Info', 'Valor']]


            header_T = header.set_index('Info').T

            float_cols = ['Área Terreno', 'Área Construída', 'Área Fundação', 'Área Fachada', 'Área Parede', 'Qtde BWCs']
            header_T = self._convert_values_to_float(header_T, float_cols)
            #add a new column to the header_T DataFrame with the file name as the first column
            header_T.insert(0, 'File', name.replace('.csv', ''))

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
            df = self._convert_money_columns_to_float(df, price_columns)

            key_name = name.replace('.csv', '')
            self.dfs[key_name] = {
                'header': header,
                'header_T': header_T,
                'budget': df
            }
    
    def _compile_T_headers(self):
        headers = []
        for key in self.dfs:
            headers.append(self.dfs[key]['header_T'])
        return pd.concat(headers)