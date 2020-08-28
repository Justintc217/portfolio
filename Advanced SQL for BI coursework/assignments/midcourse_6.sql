-- goal: gsearch lander test - estimate revenue earned by test
-- Q: revenue gain of lander compared to home (order difference) * price

USE mavenfuzzyfactory;

SELECT
    (@cvr_dif) * COUNT(DISTINCT t1.website_session_id) * MAX(t2.price_usd) AS revenue_gain_from_test,
    COUNT(DISTINCT t1.website_session_id) * @cvr_dif,
    MAX(t2.price_usd)
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
	LEFT JOIN website_pageviews AS t3
		ON t1.website_session_id = t3.website_session_id
WHERE t1.utm_source="gsearch"
    AND t1.utm_campaign="nonbrand"
    AND t3.website_pageview_id > @pv_end_of_home
    AND t1.created_at < "2012-11-27";
    
    
-- find pv where test begins
SELECT
    @pv_start_of_lander := MIN(t2.website_pageview_id)
FROM website_sessions AS t1
	LEFT JOIN website_pageviews AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.utm_source="gsearch"
    AND t1.utm_campaign="nonbrand"
    AND t2.pageview_url = "/lander-1";
    
-- find pv where test end
SELECT
    @pv_end_of_home := MAX(t2.website_pageview_id)
FROM website_sessions AS t1
	LEFT JOIN website_pageviews AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.utm_source="gsearch"
    AND t1.utm_campaign="nonbrand"
    AND t2.pageview_url = "/home";

-- find cvr for home and lander during test period
WITH lander_page_sessions AS (
SELECT
	t2.pageview_url AS lander_page,
    t2.website_session_id
FROM website_sessions AS t1
	LEFT JOIN website_pageviews AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.utm_source="gsearch"
    AND t1.utm_campaign="nonbrand"
    AND t2.website_pageview_id > @pv_start_of_lander
    AND t1.created_at < "2012-07-28"
    AND t2.pageview_url IN ("/home", "/lander-1")
),
cvr_comparison AS (
SELECT
	t2.lander_page,
    COUNT(t1.website_session_id) AS sessions,
    COUNT(t3.order_id) AS orders,
    COUNT(t3.order_id)/COUNT(t1.website_session_id) AS session_to_order_conv_rate
FROM website_sessions AS t1
	INNER JOIN lander_page_sessions AS t2
		ON t1.website_session_id = t2.website_session_id
	LEFT JOIN orders AS t3
		ON t1.website_session_id = t3.website_session_id
GROUP BY t2.lander_page
)
SELECT
	@cvr_dif := t1.session_to_order_conv_rate - t2.session_to_order_conv_rate
FROM cvr_comparison AS t1
	INNER JOIN cvr_comparison AS t2
		ON t1.lander_page <> t2.lander_page 
        AND t1.session_to_order_conv_rate > t2.session_to_order_conv_rate;
        
