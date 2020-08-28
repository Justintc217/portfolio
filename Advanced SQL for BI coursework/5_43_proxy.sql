-- get bounce rate, home sessions, lander sessions by week start date
-- from june 1st to aug 31

-- get first page

SELECT
    MIN(DATE(t1.created_at)) AS week_start_date,
    {h.bounces("t2.pageviews")}/COUNT(t1.website_session_id) AS bounce_rate,
    COUNT(CASE WHEN t1.pageview_url = '/home' THEN t1.pageview_url ELSE NULL END) AS home_sessions,
    COUNT(CASE WHEN t1.pageview_url = '/lander-1' THEN t1.pageview_url ELSE NULL END) AS lander_sessions
FROM website_pageviews AS t1
	INNER JOIN ({h.get_landing_pages("2012-06-01", "2012-08-31")}) AS t2
		ON t1.website_pageview_id = t2.first_pageview
GROUP BY WEEK(t1.created_at)
