import pandas as pd

def transform_data(df):
    df=df.copy()
    df.columns=df.columns.str.strip().str.replace(r'\s+','_',regex=True)
    if 'Demand_Forecast' in df.columns: df=df.drop(columns=['Demand_Forecast'])
    if 'Date' in df.columns: df['Date']=pd.to_datetime(df['Date'],errors='coerce')
    numeric=['Inventory_Level','Units_Sold','Units_Ordered','Price','Discount','Competitor_Pricing']
    for c in numeric:
        if c in df.columns:
            df[c]=pd.to_numeric(df[c],errors='coerce')
            df.loc[df[c]<0,c]=pd.NA
    return df.drop_duplicates().dropna().reset_index(drop=True)
