import sqlite3

def load_sqlite(df, database_path):
    with sqlite3.connect(database_path) as conn:
        df.to_sql('inventory_data',conn,if_exists='replace',index=False)
