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

    def aggregate_header_totals(self):
        headers = self.data_loader._compile_T_headers()
        total_costs = []
        total_material_costs = []
        total_execution_costs = []

        for _, header_row in headers.iterrows():
            budget_key = header_row['File']
            table_budget = self.data_loader.dfs[budget_key]['budget']

            # Calculate total cost for this specific budget table
            total_cost = table_budget['Preço (Total)'].sum()

            #do the same for the other two columns Preço Material (Total) and Preço Execução (Total)
            total_material_cost = table_budget['Preço Material (Total)'].sum()
            total_execution_cost = table_budget['Preço Execução (Total)'].sum()


            total_costs.append(total_cost)
            total_material_costs.append(total_material_cost)
            total_execution_costs.append(total_execution_cost)

              # Optional: Print for verification

        
        headers['Total Material Cost'] = total_material_costs
        headers['Total Execution Cost'] = total_execution_costs
        headers['Total Cost'] = total_costs

        return headers


    