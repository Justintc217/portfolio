

SELECT
	CASE
		WHEN t1.created_at BETWEEN "2013-11-12" AND "2013-12-12" THEN "pre_birthday_bear"
		WHEN t1.created_at BETWEEN "2013-12-12" AND "2014-01-12" THEN "post_birthday_bear"
        ELSE null
	END AS time_period,
    COUNT(t2.order_id)/COUNT(t1.website_session_id) AS conv_rate,
    AVG(t2.price_usd) AS aov,
    AVG(t2.items_purchased) AS products_per_order,
    SUM(t2.price_usd)/COUNT(t1.website_session_id) AS revenue_per_session
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.created_at BETWEEN "2013-11-12" AND "2014-01-12"
GROUP BY time_period
