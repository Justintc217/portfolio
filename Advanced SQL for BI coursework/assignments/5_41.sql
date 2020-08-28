USE mavenfuzzyfactory;

DROP TEMPORARY TABLE bounced_sessions;
DROP TEMPORARY TABLE bounced_by_landing_page;

CREATE TEMPORARY TABLE bounced_sessions AS
SELECT
    MIN(website_pageview_id) AS first_pageview,
    CASE
		WHEN COUNT(website_pageview_id) = 1 THEN "bounce"
        ELSE NULL
	END AS bounced_views
FROM website_pageviews
	INNER JOIN website_sessions
		ON website_pageviews.website_session_id = website_sessions.website_session_id
WHERE website_pageviews.created_at < "2012-07-28"
	AND website_pageview_id > 23504
	AND utm_source = "gsearch"
    AND utm_campaign = "nonbrand"
GROUP BY website_pageviews.website_session_id;

CREATE TEMPORARY TABLE bounced_by_landing_page AS
SELECT
	t1.pageview_url AS landing_page,
	t2.bounced_views
FROM website_pageviews AS t1
	INNER JOIN bounced_sessions AS t2
		ON t1.website_pageview_id = t2.first_pageview;

SELECT
	landing_page,
	COUNT(landing_page) AS sessions,
    COUNT(bounced_views) AS bounced_sessions,
    COUNT(bounced_views)/COUNT(landing_page) AS bounce_rate
FROM bounced_by_landing_page
GROUP BY landing_page;


-- SELECT
-- 	MIN(website_pageview_id),
--     MIN(created_at)
-- FROM
-- 	website_pageviews
-- WHERE
-- 	pageview_url = '/lander-1';
