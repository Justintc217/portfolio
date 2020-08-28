-- goal: sessions, conv rate, and rev per session row split by new or repeated session
-- 2014, ending nov 8th

WITH users_2014 AS (
SELECT
	DISTINCT user_id
FROM website_sessions
WHERE created_at BETWEEN "2014-01-01" AND "2014-11-08"
-- 	AND is_repeat_session=0 #uncomment to assume users have first session in 2014 only
)
SELECT
	t1.is_repeat_session,
    COUNT(t1.website_session_id) AS sessions,
    COUNT(t3.order_id) AS orders,
    COUNT(t3.order_id)/COUNT(t1.website_session_id) AS conv_rate,
    SUM(price_usd)/COUNT(t1.website_session_id) AS rev_per_session
FROM website_sessions AS t1
	INNER JOIN users_2014 AS t2
		ON t1.user_id = t2.user_id
	LEFT JOIN orders AS t3
		ON t1.website_session_id = t3.website_session_id
WHERE t1.created_at BETWEEN "2014-01-01" AND "2014-11-08"
GROUP BY t1.is_repeat_session