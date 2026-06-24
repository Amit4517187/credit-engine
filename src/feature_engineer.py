import pandas as pd
import numpy as np

def aggregate_bureau(bureau):
    return bureau.groupby('SK_ID_CURR').agg(
        bureau_loan_count = ('SK_ID_BUREAU', 'count'),
        bureau_credit_sum = ('AMT_CREDIT_SUM', 'sum'),
        bureau_overdue_sum = ('AMT_CREDIT_SUM_OVERDUE', 'sum'),
        bureau_active_loan = ('CREDIT_ACTIVE', lambda x: (x == 'Active').sum())
    ).reset_index()

def aggregate_prev(prev):
    return prev.groupby('SK_ID_CURR').agg(
        prev_amount_count = ('SK_ID_PREV', 'count'),
        prev_approved = ('NAME_CONTRACT_STATUS', lambda x: (x == 'Approved').sum()),
        prev_refused = ('NAME_CONTRACT_STATUS', lambda x: (x == 'Refused').sum()),
        prev_amt_mean = ('AMT_APPLICATION', 'mean')
    ).reset_index()

def engineer_features(data):
    df = data['app'].copy()
    df = df.merge(aggregate_bureau(data['bureau']), on ='SK_ID_CURR' , how = 'left')
    df = df.merge(aggregate_prev(data['prev']), on = 'SK_ID_CURR' , how = 'left')
    numeric_cols = df.select_dtypes(include = [np.number]).columns.tolist()
    df = df[numeric_cols].fillna(df.select_dtypes(include = [np.number]).median())
    return df

if __name__ == '__main__':
    from data_loader import load_data
    data = load_data('data/')
    df = engineer_features(data)
    print(df.head())
    print(df.shape)
    print(df.isnull().sum().sum())
    
