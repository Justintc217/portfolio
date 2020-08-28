-- goal: conversion funnel split by landing page

USE mavenfuzzyfactory;

-- SELECT
-- 	website_session_id,
-- 	pageview_url
-- FROM website_pageviews
-- WHERE pageview_url IN ("/home","/lander-1");


WITH flags_by_session AS (
SELECT
	t1.website_session_id,
    CASE 
		WHEN t1.pageview_url = '/lander-1' THEN "/lander-1"
		WHEN t1.pageview_url = '/home' THEN "/home"
        ELSE NULL
	END AS landing_page,
	(CASE WHEN t1.pageview_url = '/lander-1' THEN 1 ELSE 0 END) AS lander_flag,
	(CASE WHEN t1.pageview_url = '/home' THEN 1 ELSE 0 END) AS home_flag,
	(CASE WHEN t1.pageview_url = '/products' THEN 1 ELSE 0 END) AS products_flag,
	(CASE WHEN t1.pageview_url = '/the-original-mr-fuzzy' THEN 1 ELSE 0 END) AS mrfuzzy_flag,
	(CASE WHEN t1.pageview_url = '/cart' THEN 1 ELSE 0 END) AS cart_flag,
	(CASE WHEN t1.pageview_url = '/shipping' THEN 1 ELSE 0 END) AS shipping_flag,
	(CASE WHEN t1.pageview_url = '/billing' THEN 1 ELSE 0 END) AS billing_flag,
	(CASE WHEN t1.pageview_url = '/thank-you-for-your-order' THEN 1 ELSE 0 END) AS thankyou_flag
FROM website_sessions AS t2
	LEFT JOIN website_pageviews AS t1
		ON t1.website_session_id = t2.website_session_id
WHERE t1.created_at BETWEEN "2012-06-19" AND "2012-07-28"
	AND t2.utm_source = "gsearch"
    AND t2.utm_campaign = "nonbrand"
),
clickthrough_detail AS (
SELECT
	landing_page,
	website_session_id,
	MAX(lander_flag) AS to_lander,
	MAX(home_flag) AS to_home,
	MAX(products_flag) AS to_products,
	MAX(mrfuzzy_flag) AS to_mrfuzzy,
	MAX(cart_flag) AS to_cart,
	MAX(shipping_flag) AS to_shipping,
	MAX(billing_flag) AS to_billing,
	MAX(thankyou_flag) AS to_thankyou
FROM flags_by_session
GROUP BY website_session_id
),
clickthrough_aggregate AS (
SELECT
	landing_page,
	COUNT(website_session_id) AS sessions,
	SUM(to_lander) AS amt_to_lander,
	SUM(to_home) AS amt_to_home,
	SUM(to_products) AS amt_to_products,
	SUM(to_mrfuzzy) AS amt_to_mrfuzzy,
	SUM(to_cart) AS amt_to_cart,
	SUM(to_shipping) AS amt_to_shipping,
	SUM(to_billing) AS amt_to_billing,
	SUM(to_thankyou) AS amt_to_thankyou
FROM clickthrough_detail
GROUP BY landing_page
)
SELECT
	landing_page,
	CASE
		WHEN landing_page="/home" THEN amt_to_products/amt_to_home
		WHEN landing_page="/lander-1" THEN amt_to_products/amt_to_lander
        ELSE NULL
	END AS lander_click_rt,
	amt_to_mrfuzzy/amt_to_products AS products_click_rt,
	amt_to_cart/amt_to_mrfuzzy AS mrfuzzy_click_rt,
	amt_to_shipping/amt_to_cart AS cart_click_rt,
	amt_to_billing/amt_to_shipping AS shipping_click_rt,
	amt_to_thankyou/amt_to_billing AS billing_click_rt
FROM
	clickthrough_aggregate