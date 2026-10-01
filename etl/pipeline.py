import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / 'data/raw/retail_store_inventory.csv'
DB_FILE = BASE_DIR / 'data/processed/inventory.db'
REPORT_DIR = BASE_DIR / 'reports'


def extract():
    return pd.read_csv(RAW_FILE)


def transform(df):
    df = df.copy()
    original_rows = len(df)
    df.columns = df.columns.str.strip().str.replace(r'\s+', '_', regex=True)

    removed = 'Demand_Forecast' in df.columns
    if removed:
        df = df.drop(columns=['Demand_Forecast'])

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    numeric = ['Inventory_Level','Units_Sold','Units_Ordered','Price','Discount','Competitor_Pricing']
    for col in numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates()

    negative_counts = {}
    for col in numeric:
        if col in df.columns:
            n = int((df[col] < 0).sum())
            negative_counts[col] = n
            if n:
                df.loc[df[col] < 0, col] = pd.NA

    null_rows = int(df.isna().any(axis=1).sum())
    df = df.dropna().reset_index(drop=True)

    outliers = []
    for col in numeric:
        if col in df.columns:
            q1 = df[col].quantile(.25)
            q3 = df[col].quantile(.75)
            iqr = q3 - q1
            upper = q3 + 1.5 * iqr
            outliers.append({'campo':col,'Q1':q1,'Q3':q3,'IQR':iqr,'limite_superior':upper,'atipicos_superiores':int((df[col]>upper).sum()),'tratamiento':'Conservar'})

    return df, {'original_rows':original_rows,'duplicates':duplicates,'null_rows':null_rows,'removed_demand_forecast':removed,'negative_counts':negative_counts,'outliers':outliers}


def load(df, meta):
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_FILE) as conn:
        df.to_sql('inventory_data', conn, if_exists='replace', index=False)
        log = pd.DataFrame([{
            'fecha_ejecucion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'registros_entrada': meta['original_rows'],
            'registros_salida': len(df),
            'columnas_entrada': 15,
            'columnas_salida': len(df.columns),
            'duplicados_eliminados': meta['duplicates'],
            'filas_con_nulos_eliminadas': meta['null_rows'],
            'columna_eliminada': 'Demand Forecast' if meta['removed_demand_forecast'] else '',
            'estado': 'EXITOSO'
        }])
        log.to_sql('etl_log', conn, if_exists='replace', index=False)


def main():
    df = extract()
    clean, meta = transform(df)
    load(clean, meta)
    REPORT_DIR.mkdir(exist_ok=True)
    pd.DataFrame(meta['outliers']).to_csv(REPORT_DIR/'outliers_report.csv', index=False, encoding='utf-8-sig')
    pd.DataFrame([{'campo':k,'valores_negativos_detectados':v} for k,v in meta['negative_counts'].items()]).to_csv(REPORT_DIR/'negative_values_report.csv', index=False, encoding='utf-8-sig')
    print(f'ETL completado. Entrada: {meta["original_rows"]}; salida: {len(clean)}; duplicados: {meta["duplicates"]}; filas con nulos: {meta["null_rows"]}; Demand Forecast eliminado: {meta["removed_demand_forecast"]}')

if __name__ == '__main__':
    main()
