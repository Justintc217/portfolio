-- goal: ctr from cart page, avg products per order, average order value, 
-- ...revenue per cart page view split from month before cross sell and month after
-- cross sell initiated on sep 25th
-- cross sell - use order items page
-- cart sessions, clickthrough absolute, cart ctr, products_per_order, aov, 
-- ...rev per cart session

-- step 1: split by month b4 and after
-- step 2: get cart sessions, get after cart sessions

WITH carts_in_period AS (
SELECT
	CASE 
		WHEN created_at BETWEEN "2013-08-25" AND "2013-09-25" THEN "pre_cross_sell"
		WHEN created_at BETWEEN "2013-09-25" AND "2013-10-25" THEN "post_cross_sell"
        ELSE null
	END AS time_period,
    website_pageview_id,
	website_session_id,
	pageview_url
FROM website_pageviews
WHERE pageview_url = "/cart"
	AND created_at BETWEEN "2013-08-25" AND "2013-10-25"
),
carts_and_ctr_session_granularity AS (
SELECT
	t1.time_period,
	t1.website_session_id AS cart_session,
    MIN(t2.website_session_id) AS clickthrough
FROM carts_in_period AS t1
	LEFT JOIN website_pageviews AS t2
		ON t1.website_session_id = t2.website_session_id
        AND t2.website_pageview_id > t1.website_pageview_id
GROUP BY t1.website_session_id
)
SELECT
	t1.time_period,
    COUNT(t1.cart_session) AS cart_sessions,
    COUNT(t1.clickthrough) AS cart_clickthroughs,
    COUNT(t1.clickthrough)/COUNT(t1.cart_session) AS cart_ctr,
    AVG(t2.items_purchased) AS products_per_order,
    AVG(t2.price_usd) AS aov,
    SUM(t2.price_usd)/COUNT(t1.cart_session) AS rev_per_cart_session
FROM carts_and_ctr_session_granularity AS t1
	LEFT JOIN orders AS t2
		ON t1.cart_session = t2.website_session_id
GROUP BY t1.time_period

	