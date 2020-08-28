-- goal: nonbrand conversion rates (session -> order) split by device, g/bsearch
-- BETWEEN "2012-08-22" AND "2012-09-18"
-- also get sessions, orders
USE mavenfuzzyfactory;

SELECT
	device_type,
    utm_source,
    COUNT(t1.website_session_id) AS sessions,
	COUNT(order_id) AS orders,
    COUNT(order_id)/COUNT(t1.website_session_id) AS conv_rate
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE utm_campaign="nonbrand"
	AND utm_source IN ("gsearch","bsearch")
    AND t1.created_at BETWEEN "2012-08-22" AND "2012-09-19"
GROUP BY
	device_type,
    utm_source
ORDER BY
	device_type,
    utm_source
