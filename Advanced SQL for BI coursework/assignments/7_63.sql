-- goal: get count of sales, total revenue, and total margin (profit?) row split by months
-- margin is price - cogs
-- before jan 4th

SELECT
	YEAR(created_at) AS yr,
	MONTHNAME(created_at) AS mo,
	COUNT(order_id) AS number_of_orders,
	SUM(items_purchased) AS number_of_items_sold,
    SUM(price_usd) AS revenue,
    SUM(price_usd - cogs_usd) AS margin
FROM orders
WHERE created_at < "2013-01-04"
GROUP BY 1,2