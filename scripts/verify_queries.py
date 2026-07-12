import sqlite3
import pandas as pd

def verify():
   import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    db_path = os.path.join(BASE_DIR, 'data', 'processed', 'superstore.db')
    conn = sqlite3.connect(db_path)
    
    queries = {
        "Monthly Sales & Profit": os.path.join(BASE_DIR, 'sql', 'monthly_sales_profit.sql'),
        "Product Performance Rank": os.path.join(BASE_DIR, 'sql', 'product_performance.sql'),
        "Customer RFM Segmentation": os.path.join(BASE_DIR, 'sql', 'customer_segmentation.sql')
    }
    
    for name, path in queries.items():
        print(f"\n--- Testing Query: {name} ---")
        with open(path, 'r', encoding='utf-8') as f:
            query = f.read()
        try:
            df = pd.read_sql_query(query, conn)
            print(f"Success! Result shape: {df.shape}")
            print(df.head(5))
        except Exception as e:
            print(f"Error running query {name}: {e}")
            
    conn.close()

if __name__ == "__main__":
    verify()
