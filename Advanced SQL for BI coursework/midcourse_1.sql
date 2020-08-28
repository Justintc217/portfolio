-- goal: monthly trends for gsearch sessions and orders
-- nov 27 asked

SELECT
	MIN(DATE(t1.created_at)) AS start_month_date,
	COUNT(t1.website_session_id) AS sessions,
	COUNT(t2.order_id) AS orders
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.utm_source="gsearch"
	AND t1.created_at < "2012-11-07"
GROUP BY
	YEAR(t1.created_at),
	MONTH(DATE_ADD(t1.created_at, INTERVAL -18 DAY));
    
