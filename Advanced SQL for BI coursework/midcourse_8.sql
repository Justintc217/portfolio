-- goal: quantify impact on billing test. Revenue per billing page session
-- test from sep 10 to nov 10. Also get billing page sessions for past month
-- just use the testing dates given
-- they never switched from one billing to another conclusively (as of nov 27)
-- step 1: get only sessions with billing pages during test period
-- step 2: compare billing page to order result conversions (billing--> order) AS billing_to_order_conv_rt_lift
-- step 3: billing_to_order_conv_rt_lift * price_usd

WITH sessions_with_billings AS (
-- get billing page sessions
SELECT
	website_session_id,
    pageview_url
FROM website_pageviews
WHERE pageview_url IN ("/billing","/billing-2")
	AND created_at BETWEEN "2012-09-10" AND "2012-11-10"
),
conv_rt_by_billings AS (
-- get conversion rates by billing page version
SELECT
	t1.pageview_url,
	COUNT(t1.website_session_id) AS billing_sessions,
    COUNT(t2.order_id) AS orders,
    COUNT(t2.order_id)/COUNT(t1.website_session_id) AS billing_to_order_conv_rt
FROM sessions_with_billings AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
GROUP BY t1.pageview_url
)
-- get difference in billing page conversion rates
SELECT
	@billing_to_order_conv_rt_lift :=
    t1.billing_to_order_conv_rt - t2.billing_to_order_conv_rt
FROM conv_rt_by_billings AS t1
	INNER JOIN conv_rt_by_billings AS t2
		ON t1.pageview_url <> t2.pageview_url 
        AND t1.billing_to_order_conv_rt > t2.billing_to_order_conv_rt
;

-- revenue lift from using billing2 per billing page
SELECT
	@billing_to_order_conv_rt_lift * MIN(price_usd),
    MIN(price_usd)
FROM orders
WHERE created_at < "2012-11-27";

-- billing sessions in past month
SELECT
	pageview_url,
    COUNT(website_session_id)
FROM website_pageviews
WHERE pageview_url IN ("/billing","/billing-2")
	AND created_at BETWEEN "2012-09-10" AND "2012-11-10";

	