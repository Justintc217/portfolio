-- group website sessions by pageview url
-- order_hit per session

-- determine first pv_id for when billing-2 began use
SELECT
	MIN(website_pageview_id)
FROM website_pageviews
WHERE pageview_url="/billing-2";

-- solution: use max to search for any instance of a billing throughout all url visits per session.
-- do the same for thank you orders
WITH billing_urls_only AS (
SELECT
	MAX(CASE 
		WHEN pageview_url LIKE "%billing%" THEN pageview_url
		ELSE NULL
	END) AS billing_version,
    website_session_id,
    MAX(CASE WHEN pageview_url = "/thank-you-for-your-order" THEN website_session_id ELSE NULL END) AS order_hit
FROM website_pageviews
WHERE website_pageview_id >= 53550 AND created_at < "2012-11-10"
GROUP BY website_session_id
)
SELECT
	billing_version,
    COUNT(DISTINCT website_session_id) AS sessions,
    COUNT(DISTINCT order_hit) AS orders,
    COUNT(DISTINCT order_hit)/COUNT(DISTINCT website_session_id) AS billing_to_order_rt
FROM billing_urls_only
WHERE billing_version IS NOT NULL
GROUP BY billing_version
