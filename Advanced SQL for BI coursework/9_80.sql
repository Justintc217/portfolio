
WITH session_by_product_seen AS (
SELECT
	website_session_id,
	CASE 
		WHEN pageview_url="/the-original-mr-fuzzy" THEN "mrfuzzy"
		WHEN pageview_url="/the-forever-love-bear" THEN "lovebear" 
        ELSE NULL 
	END AS product_seen
FROM website_pageviews
WHERE pageview_url IN ("/the-original-mr-fuzzy","/the-forever-love-bear")
	AND created_at BETWEEN "2013-01-06" AND "2013-04-10"
),
absolute_funnel AS (
SELECT
	t2.product_seen,
    COUNT(DISTINCT t1.website_session_id) AS sessions,
    COUNT(CASE WHEN t1.pageview_url="/cart" THEN t1.website_session_id ELSE NULL END) AS to_cart,
    COUNT(CASE WHEN t1.pageview_url="/shipping" THEN t1.website_session_id ELSE NULL END) AS to_shipping,
    COUNT(CASE WHEN t1.pageview_url IN ("/billing","/billing-2") THEN t1.website_session_id ELSE NULL END) AS to_billing,
    COUNT(CASE WHEN t1.pageview_url="/thank-you-for-your-order" THEN t1.website_session_id ELSE NULL END) AS to_thankyou
FROM website_pageviews AS t1
	INNER JOIN session_by_product_seen AS t2
		ON t1.website_session_id = t2.website_session_id
GROUP BY t2.product_seen
)
SELECT
	product_seen,
	to_cart/sessions AS product_page_click_rt,
	to_shipping/to_cart AS cart_click_rt,
	to_billing/to_shipping AS shipping_click_rt,
	to_thankyou/to_billing AS billing_click_rt
FROM absolute_funnel
;
	

