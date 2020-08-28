-- goal: revenue, margin, total sales and revenue (same thing in this case) row split by month and product
-- reformatted in excel as final5
-- margin is revenue - cost per order

SELECT
	YEAR(created_at) AS yr,
	MONTH(created_at) AS mo,
    product_id,
    AVG(price_usd) AS revenue_per_product,
    AVG(price_usd - cogs_usd) AS margin_by_product,
    SUM(price_usd) AS total_revenue
FROM order_items
GROUP BY
	YEAR(created_at),
	MONTH(created_at),
    product_id