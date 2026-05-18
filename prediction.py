# pyrefly: ignore [missing-import]
import joblib
# pyrefly: ignore [missing-import]
import numpy as np

def prediction_analysis(df_prediction, sku_list, unit_price):
    model = joblib.load('model/model_final.pkl')
    prediction_result = model.predict(df_prediction)

    next_month_demand = {sku: int(np.round(pred)) for sku, pred in zip(sku_list, prediction_result)}

    print("Demand Prediction")
    for sku, qty in next_month_demand.items():
        print(f"{sku} : {qty} unit")
    print("\nNew Unit Price Average:")
    for sku, harga in unit_price.items():
        print(f"{sku} : $ {harga:,.2f}")

    return next_month_demand