import pandas as pd
class DataProcessor:
    def __init__(self, data_loader):
        self.data_loader = data_loader

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
