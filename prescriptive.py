# pyrefly: ignore [missing-import]
import pulp
# pyrefly: ignore [missing-import]
import numpy as np

def prescriptive_analysis(unit_price, next_month_demand, restock_budget, inventory_capacity, profit_margin):
    model = pulp.LpProblem("Optimasi_Restock_Toko_Elektronik", pulp.LpMaximize)

    amount = {
        sku: pulp.LpVariable(f"Beli_{sku}", lowBound=10, cat='Integer') 
        for sku in next_month_demand.keys()
    }

    model += pulp.lpSum([amount[sku] * unit_price[sku] * profit_margin for sku in next_month_demand.keys()]), "Total_Profit"
    model += pulp.lpSum([amount[sku] * unit_price[sku] for sku in next_month_demand.keys()]) <= restock_budget, "Budget_Limit"
    model += pulp.lpSum([amount[sku] for sku in next_month_demand.keys()]) <= inventory_capacity, "Inventory_Limit"

    for sku in next_month_demand.keys():
        model += amount[sku] <= next_month_demand[sku], f"Batas_Demand_{sku}"

    model.solve()

    print(f"Model Status: {pulp.LpStatus[model.status]}")
    print(f"Base Budget: ${restock_budget:,.2f}")
    print(f"Inventory Capacity: {inventory_capacity} unit\n")

    print("Next Month's Restock Recommendations\n")
    total_biaya = 0
    total_unit = 0

    for sku in next_month_demand.keys():
        unit_dibeli = int(amount[sku].varValue)
        biaya = unit_dibeli * unit_price[sku]
        
        total_biaya += biaya
        total_unit += unit_dibeli
        
        print(f"{sku}: Buy {unit_dibeli} unit (Demand Prediction: {next_month_demand[sku]} unit)")

    print(f"\nTotal budget used: ${total_biaya:,.2f}")
    print(f"Budget Leftovers: ${restock_budget - total_biaya:,.2f}")
    print(f"Total Unit in Inventory: {total_unit} unit")
    print(f"Estimated Profit: ${pulp.value(model.objective):,.2f}")