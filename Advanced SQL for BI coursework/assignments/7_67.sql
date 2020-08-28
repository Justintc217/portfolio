SELECT
	YEAR(t1.created_at) AS yr,
	MONTH(t1.created_at) AS mo,
	COUNT(t1.website_session_id) AS sessions,
    COUNT(t2.order_id) AS orders
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.created_at < "2013-01-01"
GROUP BY
	MONTH(t1.created_at)
ORDER BY
	MONTH(t1.created_at)
;

SELECT
    MIN(DATE(t1.created_at)) AS week_start_date,
	COUNT(t1.website_session_id) AS sessions,
    COUNT(t2.order_id) AS orders
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.created_at < "2013-01-01"
GROUP BY
    WEEK(t1.created_at)
ORDER BY
    WEEK(t1.created_at);