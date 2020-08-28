-- goal: session_to_order_conv_rate, revenue per session, product 1 order count, product 2 order count
-- split by month
-- april 1st 2012 to april 5th 2013

SELECT
	YEAR(t1.created_at) AS yr,
    MONTHNAME(t1.created_at) AS mo,
    COUNT(t1.website_session_id) AS sessions,
    COUNT(t2.order_id) AS orders,
    COUNT(t2.order_id)/COUNT(t1.website_session_id) AS conv_rate,
    SUM(t2.price_usd)/COUNT(t1.website_session_id) AS revenue_per_session,
    COUNT(CASE WHEN t2.primary_product_id = 1 THEN order_id ELSE NULL END) AS product_one_orders,
    COUNT(CASE WHEN t2.primary_product_id = 2 THEN order_id ELSE NULL END) AS product_two_orders
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.created_at BETWEEN "2012-04-01" AND "2013-04-05"
GROUP BY 1,2