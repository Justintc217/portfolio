-- goal: billing to order conversion rate (eg. billings/orders) for billing and billing-2
-- step 1: limit time between (first pageview_url has pv = 53550 and web id = 25325) and "2012-11-10"
-- note that this is for all search customers
-- step 2: pivot for billing urls (count case when pv_url=billing)
-- also get count of pv_url=thankyou. 
-- also get count of sessions

-- Q: is thankyou same as orders
-- Q: can a single session have multiple billing pv_urls (eg. billing --> home --> billing)
-- R: can resolve with using - count distinct of case when pv_url=billing then pv_id

-- pvurls must all be analyzed in the same session. for each session was there a billing, thankyou

WITH url_flags AS (
SELECT 
    website_session_id,
    MAX(CASE WHEN pageview_url="/billing" THEN website_pageview_id ELSE NULL END) AS billing_hit,
    MAX(CASE WHEN pageview_url="/billing-2" THEN website_pageview_id ELSE NULL END) AS billing2_hit,
    MAX(CASE WHEN pageview_url="/thank-you-for-your-order" THEN website_pageview_id ELSE NULL END) AS thankyou_hit
FROM website_pageviews
WHERE website_pageview_id >= 53550 AND created_at < "2012-11-10"
GROUP BY website_session_id
)
SELECT
	CASE
		WHEN t2.billing_hit IS NOT NULL THEN "/billing"
        WHEN t2.billing2_hit IS NOT NULL THEN "/billing-2"
	END AS billing_version,
    COUNT(DISTINCT t2.website_session_id) AS sessions,
    COUNT(DISTINCT thankyou_hit) AS orders,
    COUNT(DISTINCT thankyou_hit)/COUNT(DISTINCT t2.website_session_id) AS billing_to_order_rt
FROM website_pageviews AS t1
	INNER JOIN url_flags AS t2
		ON t1.website_session_id = t2.website_session_id
GROUP BY billing_version
HAVING billing_version IS NOT NULL
