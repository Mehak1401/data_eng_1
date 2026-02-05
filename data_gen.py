import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import random
from datetime import datetime, timedelta

def generate_data(num_rows=16000):
    print(f"Generating {num_rows} rows of synthetic data...")
    
    # Generate user_ids
    user_ids = np.random.randint(1000, 9999, size=num_rows)
    
    # Generate product categories
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Toys']
    product_categories = np.random.choice(categories, size=num_rows)
    
    # Generate prices (random float between 10.0 and 1000.0)
    prices = np.round(np.random.uniform(10.0, 1000.0, size=num_rows), 2)
    
    # Generate status
    statuses = ['completed', 'pending', 'cancelled', 'refunded']
    status_choices = np.random.choice(statuses, size=num_rows, p=[0.7, 0.2, 0.05, 0.05])
    
    # Generate timestamps (within last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Random timestamps
    timestamps = []
    for _ in range(num_rows):
        random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
        timestamps.append(start_date + timedelta(seconds=random_seconds))
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'user_id': user_ids,
        'product_category': product_categories,
        'price': prices,
        'status': status_choices
    })
    
    # Introduce some missing values (approx 1% of prices)
    mask = np.random.choice([True, False], size=num_rows, p=[0.01, 0.99])
    df.loc[mask, 'price'] = np.nan
    
    # Save to Parquet
    table = pa.Table.from_pandas(df)
    pq.write_table(table, 'raw_data.parquet')
    
    print(f"Data generated and saved to 'raw_data.parquet'. Rows: {len(df)}")

if __name__ == "__main__":
    generate_data()
