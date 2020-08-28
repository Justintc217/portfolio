-- goal: session to order conversion rates by month
-- over first 8 months
-- step 1: find start date and limit created by between start date and start + 8mo
-- step 2: join orders and website_sessions
-- step 3: group by month created_at
-- also get month name, year of each date in month increment

-- USE mavenfuzzyfactory;

-- set start date
-- SELECT
-- 	@start_date := DATE(MIN(created_at))
-- FROM website_sessions;

SELECT
    DATE(MIN(t1.created_at)) AS month_date_start,
    COUNT(t2.order_id)/COUNT(t1.website_session_id) AS session_to_order_conv_rt
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.created_at < DATE_ADD(@start_date, INTERVAL 8 MONTH)
GROUP BY 
	YEAR(t1.created_at),
	MONTH(DATE_ADD(t1.created_at, INTERVAL -18 DAY))

