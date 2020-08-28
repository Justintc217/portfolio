-- goal for project 3: monthly trend for gsearch nonbrand split by device type

SELECT
	MIN(DATE(t1.created_at)) AS start_month_date,
    t1.utm_campaign,
    t1.device_type,
	COUNT(t1.website_session_id) AS sessions,
	COUNT(t2.order_id) AS orders
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.utm_source="gsearch"
	AND utm_campaign="nonbrand"
	AND t1.created_at < "2012-11-27"
GROUP BY
	YEAR(t1.created_at),
	MONTH(DATE_ADD(t1.created_at, INTERVAL -18 DAY)),
    t1.device_type
ORDER BY
	YEAR(t1.created_at),
	MONTH(DATE_ADD(t1.created_at, INTERVAL -18 DAY)),
    t1.device_type
;