# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from data import data_setup
from prediction import prediction_analysis
from prescriptive import prescriptive_analysis

st.set_page_config(page_title="GDKB BI - Restock Optimizer", layout="wide")

st.title("Smart Electronic Store Restock Optimizer")
st.write("This application predicts next month's demand and provides optimal restock recommendations based on your budget and inventory capacity.")

# Sidebar for inputs
st.sidebar.header("User Inputs")

# File upload for dataset
uploaded_file = st.sidebar.file_uploader("Upload Dataset (CSV)", type=['csv'])

data_source = uploaded_file
restock_budget = st.sidebar.number_input("Restock Budget ($)", value=1000000, step=10000)
inventory_capacity = st.sidebar.number_input("Inventory Capacity (units)", value=10000, step=100)
profit_margin = st.sidebar.slider("Profit Margin", min_value=0.01, max_value=1.0, value=0.3, step=0.01)

if st.sidebar.button("Run Optimizer"):
    with st.spinner("Analyzing data and predicting demand..."):
        try:
            # Data Preparation
            df_prediction, sku_list, unit_price = data_setup(data_source, 'context/training_col.pkl')
            
            # Prediction
            next_month_demand = prediction_analysis(df_prediction, sku_list, unit_price)
            
            # Prescriptive
            results = prescriptive_analysis(unit_price, next_month_demand, restock_budget, inventory_capacity, profit_margin)
            
            st.success(f"Optimization Completed: {results['status']}")
            
            # Layout for top-level metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Budget Used", f"${results['total_budget_used']:,.2f}")
            col2.metric("Budget Leftovers", f"${results['budget_leftovers']:,.2f}")
            col3.metric("Total Unit in Inventory", f"{results['total_unit_in_inventory']} units")
            col4.metric("Estimated Profit", f"${results['estimated_profit']:,.2f}")
            
            st.markdown("---")
            
            # Detailed Recommendations
            st.subheader("Next Month's Restock Recommendations")
            
            recommendations_df = []
            for sku, details in results['recommendations'].items():
                recommendations_df.append({
                    "SKU": sku,
                    "Unit Price": f"${unit_price[sku]:,.2f}",
                    "Demand Prediction": details["demand"],
                    "Recommended Buy": details["buy"],
                    "Cost": f"${details['cost']:,.2f}"
                })
            
            df_rec = pd.DataFrame(recommendations_df)
            st.dataframe(df_rec, use_container_width=True)
            
            # Show Demand Prediction & Unit Price Summary
            with st.expander("Show Demand Prediction & Unit Price Details"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Demand Prediction**")
                    st.dataframe(pd.DataFrame(list(next_month_demand.items()), columns=["SKU", "Predicted Demand"]))
                with col_b:
                    st.write("**New Unit Price Average**")
                    unit_price_df = pd.DataFrame(list(unit_price.items()), columns=["SKU", "Average Price ($)"])
                    st.dataframe(unit_price_df)
                    
        except Exception as e:
            st.error(f"An error occurred: {e}")
