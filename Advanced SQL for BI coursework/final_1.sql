SELECT
	MIN(DATE(t1.created_at)) AS quarter_start_date,
	MAX(DATE(t1.created_at)) AS quarter_end_date,
	COUNT(t1.website_session_id) AS sessions,
	COUNT(t2.order_id) AS orders,
    CASE WHEN TIMESTAMPDIFF(
		QUARTER, 
		MIN(DATE(t1.created_at)),
		MAX(DATE_ADD(t1.created_at, INTERVAL 1 DAY))
    ) = 1 THEN "full quarter" ELSE "partial quarter" END AS is_full_quarter
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
GROUP BY
	YEAR(t1.created_at),
	quarter(t1.created_at)