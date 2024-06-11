import pandas as pd

class DataLoader:
    def __init__(self):
        self.dfs = {}

    def _get_filepath(self, data_dir, file_name):
        return f"{data_dir}/{file_name}"

    def _load_data_from_path(self, data_dir, file_names):
        for name in file_names:
            path = self._get_filepath(data_dir, name)
            '''Leitor de Header - Primeiras 9 linhas'''
            header = pd.read_csv(path,skiprows=1, nrows=8, header=None)

            header = header.iloc[:, :2]
            header.columns = ['Info', 'Valor']
            header = header.dropna(subset=['Info', 'Valor'])
            header = header[['Info', 'Valor']]

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

            key_name = name.replace('.csv', '')
            self.dfs[key_name] = {
                'header': header,
                'budget': df
            }