-- goal product page sessions, clickthrough rate for /products, conv rate from /products to order row split by month

SELECT
	YEAR(t1.created_at) AS yr,
	MONTH(t1.created_at) AS mo,
	COUNT(DISTINCT t1.website_session_id) AS product_sessions,
    COUNT(DISTINCT CASE WHEN t1.website_pageview_id > t2.website_pageview_id THEN t1.website_session_id ELSE NULL END)
    AS product_clickthrough_sessions, #1 web id per case of pageview existing after /products
    COUNT(DISTINCT t3.order_id) AS orders,
    
    COUNT(DISTINCT CASE WHEN t1.website_pageview_id > t2.website_pageview_id THEN t1.website_session_id ELSE NULL END)
    /COUNT(DISTINCT t1.website_session_id) AS product_clickthrough_rate,
    
    COUNT(DISTINCT t3.order_id)/COUNT(DISTINCT t1.website_session_id) AS product_order_conv_rate
FROM website_pageviews AS t1
	INNER JOIN website_pageviews AS t2
		ON t1.website_session_id = t2.website_session_id AND t2.pageview_url="/products"
	LEFT JOIN orders AS t3
		ON t1.website_session_id = t3.website_session_id
GROUP BY
	YEAR(t1.created_at),
	MONTH(t1.created_at)