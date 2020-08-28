-- get bounce rate, home sessions, lander sessions by week start date
-- from june 1st to aug 31

-- get first page

SELECT
    MIN(DATE(t1.created_at)) AS week_start_date,
    COUNT(CASE WHEN t2.pageviews = 1 THEN t2.pageviews ELSE NULL END)/COUNT(t1.website_session_id) AS bounce_rate,
    COUNT(CASE WHEN t1.pageview_url = '/home' THEN t1.pageview_url ELSE NULL END) AS home_sessions,
    COUNT(CASE WHEN t1.pageview_url = '/lander-1' THEN t1.pageview_url ELSE NULL END) AS lander_sessions
FROM website_pageviews AS t1
	INNER JOIN (
	SELECT
		pageview_url,
		MIN(website_pageview_id) AS first_pageview,
		COUNT(website_pageview_id) AS pageviews
	FROM website_pageviews
		INNER JOIN website_sessions
			ON website_pageviews.website_session_id = website_sessions.website_session_id
	WHERE website_pageviews.created_at BETWEEN '2012-06-01' AND '2012-08-31'
		AND utm_source = 'gsearch'
		AND utm_campaign = 'nonbrand'
	GROUP BY website_sessions.website_session_id
	) AS t2
		ON t1.website_pageview_id = t2.first_pageview
GROUP BY WEEK(t1.created_at)
