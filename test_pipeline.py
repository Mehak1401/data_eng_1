import pytest
import pandas as pd
import sqlite3
import os
from data_gen import generate_data
from etl_pipeline import run_etl

@pytest.fixture(scope="module")
def setup_database():
    # Setup: Generate data and run ETL
    print("\n[Setup] Generating data and running ETL...")
    generate_data(num_rows=16000)
    run_etl()
    yield
    # Teardown (optional, we might want to keep the db for inspection)
    # os.remove('warehouse.db')
    # os.remove('raw_data.parquet')

def test_row_count(setup_database):
    """Verify that the final database has > 15,000 rows."""
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    conn.close()
    
    print(f"\n[Test] Row count in DB: {count}")
    assert count > 15000, f"Expected > 15,000 rows, but found {count}"

def test_schema_check(setup_database):
    """Ensure all expected columns exist."""
    expected_columns = {
        'timestamp', 'user_id', 'product_category', 
        'price', 'status', 'total_with_tax'
    }
    
    conn = sqlite3.connect('warehouse.db')
    df = pd.read_sql("SELECT * FROM transactions LIMIT 1", conn)
    conn.close()
    
    actual_columns = set(df.columns)
    print(f"\n[Test] Columns found: {actual_columns}")
    
    missing_columns = expected_columns - actual_columns
    assert not missing_columns, f"Missing columns: {missing_columns}"

def test_tax_calculation(setup_database):
    """Spot check tax calculation."""
    conn = sqlite3.connect('warehouse.db')
    df = pd.read_sql("SELECT price, total_with_tax FROM transactions LIMIT 5", conn)
    conn.close()
    
    for _, row in df.iterrows():
        expected_total = round(row['price'] * 1.12, 2)
        assert abs(row['total_with_tax'] - expected_total) < 0.01, \
            f"Tax calc error: Price {row['price']}, Got {row['total_with_tax']}, Expected {expected_total}"
