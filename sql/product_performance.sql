-- Analysis: Product Performance Analysis
-- Objective: Rank products by profitability within each category to identify the top 5 most profitable and top 5 least profitable (loss-making) products.

WITH ProductProfitability AS (
    SELECT 
        category,
        product_name,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        SUM(quantity) AS total_quantity
    FROM orders
    GROUP BY category, product_name
),
RankedProducts AS (
    SELECT 
        category,
        product_name,
        total_sales,
        total_profit,
        total_quantity,
        -- Rank for most profitable products (1 is highest profit)
        DENSE_RANK() OVER (PARTITION BY category ORDER BY total_profit DESC) AS profit_rank_desc,
        -- Rank for least profitable products (1 is highest loss/lowest profit)
        DENSE_RANK() OVER (PARTITION BY category ORDER BY total_profit ASC) AS profit_rank_asc
    FROM ProductProfitability
)
SELECT 
    category AS "Category",
    product_name AS "Product Name",
    total_sales AS "Sales ($)",
    total_profit AS "Profit ($)",
    total_quantity AS "Quantity Sold",
    CASE 
        WHEN profit_rank_desc <= 5 THEN 'Top 5 Profitable'
        WHEN profit_rank_asc <= 5 THEN 'Top 5 Loss-making'
    END AS "Performance Status",
    CASE 
        WHEN profit_rank_desc <= 5 THEN profit_rank_desc
        WHEN profit_rank_asc <= 5 THEN profit_rank_asc
    END AS "Rank Within Category"
FROM RankedProducts
WHERE profit_rank_desc <= 5 OR profit_rank_asc <= 5
ORDER BY 
    category, 
    "Performance Status" DESC, 
    "Rank Within Category" ASC;
