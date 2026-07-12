-- Schema definition for Superstore Orders Table
-- This table contains detailed transactions of a retail store's orders.

CREATE TABLE IF NOT EXISTS orders (
    row_id INTEGER PRIMARY KEY,             -- Unique Row Identifier
    order_id TEXT,                          -- Unique Order Identifier (e.g., CA-2016-152156)
    order_date TEXT,                        -- Date of the order (Standardized: YYYY-MM-DD)
    ship_date TEXT,                         -- Date when the order was shipped (Standardized: YYYY-MM-DD)
    ship_mode TEXT,                         -- Ship Mode (Standard Class, Second Class, First Class, Same Day)
    customer_id TEXT,                       -- Unique Customer Identifier
    customer_name TEXT,                     -- Name of the Customer
    segment TEXT,                           -- Customer Segment (Consumer, Corporate, Home Office)
    country TEXT,                           -- Country Name (e.g., United States)
    city TEXT,                              -- City name
    state TEXT,                             -- State name
    postal_code TEXT,                       -- Postal Code
    region TEXT,                            -- Geographic Region (East, West, Central, South)
    product_id TEXT,                        -- Unique Product Identifier
    category TEXT,                          -- Product Category (Technology, Furniture, Office Supplies)
    sub_category TEXT,                      -- Product Sub-Category
    product_name TEXT,                      -- Full name of the Product
    sales REAL,                             -- Sales amount (numeric)
    quantity INTEGER,                       -- Quantity of items ordered
    discount REAL,                          -- Discount rate (0.00 to 0.80)
    profit REAL                             -- Profit earned from this item (can be negative if unprofitable)
);
