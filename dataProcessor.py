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
            'Total Material Cost': total_material_cost,
            'Total Execution Cost': total_execution_cost,
            'Total Cost': total_cost
        }
