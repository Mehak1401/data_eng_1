import pandas as pd
import sqlite3
import os

def run_etl():
    print("Starting ETL Pipeline...")
    
    # EXTRACT
    if not os.path.exists('raw_data.parquet'):
        print("Error: raw_data.parquet not found. Please run data_gen.py first.")
        return
        
    print("Extracting data from raw_data.parquet...")
    df = pd.read_parquet('raw_data.parquet')
    initial_count = len(df)
    print(f"Extracted {initial_count} rows.")
    
    # TRANSFORM
    print("Transforming data...")
    
    # Handle missing values (fill price with mean or drop)
    # Strategy: Fill missing prices with the median price of the category
    df['price'] = df.groupby('product_category')['price'].transform(
        lambda x: x.fillna(x.median())
    )
    
    # If any NaNs remain (e.g., category had no prices), drop them
    df = df.dropna(subset=['price'])
    
    # Calculate total_with_tax (12%)
    TAX_RATE = 0.12
    df['total_with_tax'] = df['price'] * (1 + TAX_RATE)
    df['total_with_tax'] = df['total_with_tax'].round(2)
    
    # Cast types if needed (parquet preserves types well, but good practice)
    df['user_id'] = df['user_id'].astype(int)
    
    print(f"Transformed data. Rows after cleaning: {len(df)}")
    
    # LOAD
    print("Loading data into warehouse.db...")
    conn = sqlite3.connect('warehouse.db')
    
    # Save to SQLite
    df.to_sql('transactions', conn, if_exists='replace', index=False)
    
    conn.close()
    print("ETL Pipeline completed successfully.")

if __name__ == "__main__":
    run_etl()
