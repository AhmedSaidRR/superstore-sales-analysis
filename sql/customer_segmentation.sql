-- Analysis: Customer RFM Segmentation
-- Objective: Group customers into commercial segments based on Recency, Frequency, and Monetary metrics using CTEs.

WITH CustomerMetrics AS (
    SELECT 
        customer_id,
        customer_name,
        segment AS original_segment,
        -- Reference date is the latest date in the dataset
        (SELECT MAX(order_date) FROM orders) AS max_dataset_date,
        MAX(order_date) AS last_order_date,
        COUNT(DISTINCT order_id) AS purchase_frequency,
        ROUND(SUM(sales), 2) AS total_monetary_value,
        ROUND(SUM(profit), 2) AS total_profit_generated
    FROM orders
    GROUP BY customer_id, customer_name, original_segment
),
RFM_Calculations AS (
    SELECT 
        customer_id,
        customer_name,
        original_segment,
        purchase_frequency,
        total_monetary_value,
        total_profit_generated,
        -- Calculate Recency in days (difference between last dataset date and last customer purchase)
        CAST(julianday(max_dataset_date) - julianday(last_order_date) AS INTEGER) AS recency_days
    FROM CustomerMetrics
)
SELECT 
    customer_id AS "Customer ID",
    customer_name AS "Customer Name",
    original_segment AS "Original Segment",
    recency_days AS "Recency (Days)",
    purchase_frequency AS "Frequency (Orders)",
    total_monetary_value AS "Monetary Value ($)",
    total_profit_generated AS "Net Profit ($)",
    CASE
        WHEN recency_days <= 180 AND purchase_frequency >= 12 THEN 'Champions (Frequent & Active)'
        WHEN recency_days <= 180 AND purchase_frequency BETWEEN 6 AND 11 THEN 'Loyal Customers (Active)'
        WHEN recency_days <= 90 AND purchase_frequency < 6 THEN 'New / Recent Customers'
        WHEN recency_days > 365 THEN 'Lapsed Customers (Inactive > 1 Year)'
        WHEN recency_days BETWEEN 181 AND 365 AND purchase_frequency >= 6 THEN 'At Risk (Used to buy, now fading)'
        ELSE 'Regular Customers'
    END AS "Customer Segment Group"
FROM RFM_Calculations
ORDER BY "Monetary Value ($)" DESC;
