-- Analysis: Monthly Sales, Profit, and Profit Margin Trends
-- Objective: Understand seasonality, business growth, and profit margin trends over time.

WITH MonthlyStats AS (
    SELECT 
        strftime('%Y', order_date) AS order_year,
        strftime('%m', order_date) AS order_month,
        strftime('%Y-%m', order_date) AS year_month,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(AVG(discount) * 100, 2) AS average_discount_pct
    FROM orders
    GROUP BY order_year, order_month, year_month
)
SELECT 
    year_month AS "Month",
    total_sales AS "Sales ($)",
    total_profit AS "Profit ($)",
    ROUND((total_profit / total_sales) * 100, 2) AS "Profit Margin (%)",
    total_orders AS "Orders Count",
    average_discount_pct AS "Avg Discount (%)",
    -- Cumulative (Running) Total Sales over the entire period
    ROUND(SUM(total_sales) OVER (ORDER BY year_month), 2) AS "Running Total Sales ($)",
    -- Cumulative (Running) Total Profit over the entire period
    ROUND(SUM(total_profit) OVER (ORDER BY year_month), 2) AS "Running Total Profit ($)"
FROM MonthlyStats
ORDER BY year_month ASC;
