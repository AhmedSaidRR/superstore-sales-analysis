import csv
import sqlite3
import json
import os
from datetime import datetime

def parse_date(date_str):
    date_str = date_str.strip()
    formats = [
        "%m-%d-%Y", "%m/%d/%Y",
        "%d-%m-%Y", "%d/%m/%Y",
        "%Y-%m-%d", "%Y/%m/%d",
        "%m-%d-%y", "%m/%d/%y",
        "%d-%m-%y", "%d/%m/%y"
    ]
    
    # Try common formats
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            # Standardize to YYYY-MM-DD
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
            
    # Fallback/heuristic if formats fail
    # E.g. replacing delimiters
    cleaned_str = date_str.replace('/', '-').replace('\\', '-')
    for fmt in ["%m-%d-%Y", "%d-%m-%Y", "%Y-%m-%d"]:
        try:
            dt = datetime.strptime(cleaned_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
            
    raise ValueError(f"Could not parse date: {date_str}")

def run_etl():
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    raw_path = os.path.join(BASE_DIR, 'data', 'raw', 'superstore.csv')
    db_path = os.path.join(BASE_DIR, 'data', 'processed', 'superstore.db')
    clean_csv_path = os.path.join(BASE_DIR, 'data', 'processed', 'superstore_clean.csv')
    summary_json_path = os.path.join(BASE_DIR, 'data', 'processed', 'superstore_summary.json')
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Read raw CSV
    print(f"Reading raw data from {raw_path}...")
    cleaned_rows = []
    
    with open(raw_path, mode='r', encoding='windows-1252') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            try:
                row_id = int(row['Row ID'])
                sales = float(row['Sales'])
                quantity = int(row['Quantity'])
                discount = float(row['Discount'])
                profit = float(row['Profit'])
                
                order_date = parse_date(row['Order Date'])
                ship_date = parse_date(row['Ship Date'])
                
                cleaned_row = {
                    'row_id': row_id,
                    'order_id': row['Order ID'].strip(),
                    'order_date': order_date,
                    'ship_date': ship_date,
                    'ship_mode': row['Ship Mode'].strip(),
                    'customer_id': row['Customer ID'].strip(),
                    'customer_name': row['Customer Name'].strip(),
                    'segment': row['Segment'].strip(),
                    'country': row['Country'].strip(),
                    'city': row['City'].strip(),
                    'state': row['State'].strip(),
                    'postal_code': row['Postal Code'].strip(),
                    'region': row['Region'].strip(),
                    'product_id': row['Product ID'].strip(),
                    'category': row['Category'].strip(),
                    'sub_category': row['Sub-Category'].strip(),
                    'product_name': row['Product Name'].strip(),
                    'sales': sales,
                    'quantity': quantity,
                    'discount': discount,
                    'profit': profit
                }
                cleaned_rows.append(cleaned_row)
            except Exception as e:
                print(f"Error processing row {idx + 1}: {e}")
                
    print(f"Processed {len(cleaned_rows)} rows successfully.")
    
    # Write to SQLite
    print("Writing to SQLite database...")
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE orders (
        row_id INTEGER PRIMARY KEY,
        order_id TEXT,
        order_date TEXT,
        ship_date TEXT,
        ship_mode TEXT,
        customer_id TEXT,
        customer_name TEXT,
        segment TEXT,
        country TEXT,
        city TEXT,
        state TEXT,
        postal_code TEXT,
        region TEXT,
        product_id TEXT,
        category TEXT,
        sub_category TEXT,
        product_name TEXT,
        sales REAL,
        quantity INTEGER,
        discount REAL,
        profit REAL
    )
    """)
    
    cursor.executemany("""
    INSERT INTO orders VALUES (
        :row_id, :order_id, :order_date, :ship_date, :ship_mode,
        :customer_id, :customer_name, :segment, :country, :city,
        :state, :postal_code, :region, :product_id, :category,
        :sub_category, :product_name, :sales, :quantity, :discount, :profit
    )
    """, cleaned_rows)
    
    conn.commit()
    print("Database insert completed.")
    
    # Write to Cleaned CSV (UTF-8 encoded)
    print(f"Writing cleaned data to CSV: {clean_csv_path}")
    headers = [
        'row_id', 'order_id', 'order_date', 'ship_date', 'ship_mode',
        'customer_id', 'customer_name', 'segment', 'country', 'city',
        'state', 'postal_code', 'region', 'product_id', 'category',
        'sub_category', 'product_name', 'sales', 'quantity', 'discount', 'profit'
    ]
    with open(clean_csv_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(cleaned_rows)
    print("Clean CSV written successfully.")
    
    # Generate aggregated data for summary JSON (KPIs, Monthly, Categories, Regions)
    print("Generating aggregate metrics for dashboard summary...")
    
    # 1. Total KPIs
    cursor.execute("SELECT SUM(sales), SUM(profit), COUNT(DISTINCT order_id), AVG(discount) FROM orders")
    tot_sales, tot_profit, tot_orders, avg_discount = cursor.fetchone()
    profit_margin = (tot_profit / tot_sales) * 100 if tot_sales else 0
    
    # 2. Monthly Trend (YYYY-MM)
    cursor.execute("""
        SELECT strftime('%Y-%m', order_date) as month, SUM(sales), SUM(profit)
        FROM orders
        GROUP BY month
        ORDER BY month ASC
    """)
    monthly_trend = [{"month": r[0], "sales": r[1], "profit": r[2]} for r in cursor.fetchall()]
    
    # 3. Category Sales & Profit
    cursor.execute("""
        SELECT category, SUM(sales), SUM(profit)
        FROM orders
        GROUP BY category
        ORDER BY SUM(sales) DESC
    """)
    category_summary = [{"category": r[0], "sales": r[1], "profit": r[2]} for r in cursor.fetchall()]
    
    # 4. Regional Sales & Profit
    cursor.execute("""
        SELECT region, SUM(sales), SUM(profit)
        FROM orders
        GROUP BY region
        ORDER BY SUM(sales) DESC
    """)
    region_summary = [{"region": r[0], "sales": r[1], "profit": r[2]} for r in cursor.fetchall()]
    
    # 5. Top 10 Profitable Products
    cursor.execute("""
        SELECT product_name, SUM(sales), SUM(profit)
        FROM orders
        GROUP BY product_name
        ORDER BY SUM(profit) DESC
        LIMIT 10
    """)
    top_products = [{"product_name": r[0], "sales": r[1], "profit": r[2]} for r in cursor.fetchall()]
    
    # 6. Bottom 10 Unprofitable Products
    cursor.execute("""
        SELECT product_name, SUM(sales), SUM(profit)
        FROM orders
        GROUP BY product_name
        ORDER BY SUM(profit) ASC
        LIMIT 10
    """)
    bottom_products = [{"product_name": r[0], "sales": r[1], "profit": r[2]} for r in cursor.fetchall()]
    
    summary = {
        "kpis": {
            "total_sales": tot_sales,
            "total_profit": tot_profit,
            "total_orders": tot_orders,
            "profit_margin": profit_margin,
            "average_discount": avg_discount
        },
        "monthly_trend": monthly_trend,
        "category_summary": category_summary,
        "region_summary": region_summary,
        "top_products": top_products,
        "bottom_products": bottom_products
    }
    
    with open(summary_json_path, mode='w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4)
        
    print(f"Summary JSON written to: {summary_json_path}")
    conn.close()
    print("ETL completed successfully!")

if __name__ == "__main__":
    run_etl()
