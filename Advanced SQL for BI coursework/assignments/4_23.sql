USE mavenfuzzyfactory;

SELECT
	device_type,
	COUNT(t1.website_session_id) AS sessions,
    COUNT(t2.order_id) AS orders,
    CONCAT((COUNT(t2.order_id)/COUNT(t1.website_session_id))*100,"%") AS session_to_order_conv_rate
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.created_at < "2012-04-14" AND t1.utm_source = "gsearch" AND utm_campaign = "nonbrand"
GROUP BY device_type;



