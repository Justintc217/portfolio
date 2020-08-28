-- goal for project 4: monthly trend of orders, sessions split by utm source
WITH dates AS (
SELECT
	MIN(DATE(t1.created_at)) AS start_month_date
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.created_at < "2012-11-27"
GROUP BY
	YEAR(t1.created_at),
	MONTH(DATE_ADD(t1.created_at, INTERVAL -18 DAY))
)
SELECT
	d.start_month_date,
    t1.utm_source,
	COUNT(t1.website_session_id) AS sessions,
	COUNT(t2.order_id) AS orders
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
	LEFT JOIN dates AS d
		ON MONTH(DATE_ADD(t1.created_at, INTERVAL -18 DAY)) = MONTH(d.start_month_date)
WHERE t1.created_at < "2012-11-27"
GROUP BY
	YEAR(t1.created_at),
	MONTH(DATE_ADD(t1.created_at, INTERVAL -18 DAY)),
    t1.utm_source
ORDER BY
	YEAR(t1.created_at),
	MONTH(DATE_ADD(t1.created_at, INTERVAL -18 DAY)),
    t1.utm_source
;