import pandas as pd
# pyrefly: ignore [missing-import]
import joblib

def data_setup(data_path, default_col_path):
    df = pd.read_csv(data_path)

    df = df[df['Order Status'] == 'Completed']
    unit_price = df.groupby('SKU')['Unit Price'].mean().to_dict()

    df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
    last_month = df['Purchase Date'].max()

    next_month_goal = last_month + pd.DateOffset(months=1)
    target_year = next_month_goal.year
    target_month = next_month_goal.month

    df_prediction = df[['Product Type', 'SKU']].drop_duplicates().reset_index(drop=True)

    df_prediction['Year'] = target_year
    df_prediction['Month'] = target_month

    sku_list = df_prediction['SKU'].tolist()

    df_encoded = pd.get_dummies(df_prediction, columns=['Product Type', 'SKU'])
    df_col = joblib.load(default_col_path)

    df_final = df_encoded.reindex(columns=df_col, fill_value=0)

    return df_final, sku_list, unit_price