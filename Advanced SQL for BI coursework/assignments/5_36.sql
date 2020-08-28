USE mavenfuzzyfactory;

WITH landing_page_visits AS (
SELECT
	MIN(created_at),
    pageview_url AS landing_page
FROM
	website_pageviews
WHERE created_at < "2012-06-12"
GROUP BY website_session_id
)
SELECT
	landing_page,
	COUNT(landing_page) AS sessions_hitting_this_landing_page
FROM landing_page_visits
GROUP BY landing_page
ORDER BY sessions_hitting_this_landing_page;