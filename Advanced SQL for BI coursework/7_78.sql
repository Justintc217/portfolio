-- goal: clickthrough rates for /products
-- Q: clickthrough products is (/products --> /{specific product page})?
-- from jan 6th to april 6th 2013 
-- Q: also 3 months leading up to launch used as baseline?? so oct 2012 to april 6th 2013??
-- group results into two time periods


-- SELECT
-- 	COUNT(DISTINCT t1.website_session_id) AS w_next_pg,
-- 	t2.website_session_id,
-- 	t1.pageview_url,
-- 	t2.pageview_url,
--     t1.website_pageview_id,
-- 	t2.website_pageview_id
-- FROM website_pageviews AS t1
-- 	INNER JOIN website_pageviews AS t2
-- 		ON t1.website_pageview_id < t2.website_pageview_id AND t1.website_session_id = t2.website_session_id
-- WHERE t1.pageview_url = "/products"
-- 	AND t1.created_at BETWEEN "2012-10-06" AND "2013-04-06";
	


SELECT
	CASE
		WHEN t1.created_at BETWEEN "2012-10-06" AND "2013-01-06" THEN "before period"
		WHEN t1.created_at BETWEEN "2013-01-06" AND "2013-04-06" THEN "after period"
        ELSE NULL
	END AS periods,
    COUNT(CASE WHEN t1.pageview_url="/products" THEN t1.website_session_id ELSE NULL END) AS product_sessions,
    COUNT(CASE WHEN t1.pageview_url IN ("/the-original-mr-fuzzy","/the-forever-love-bear") THEN t1.website_session_id ELSE NULL END) AS w_next_pg,
    
    COUNT(CASE WHEN t1.pageview_url IN ("/the-original-mr-fuzzy","/the-forever-love-bear") THEN t1.website_session_id ELSE NULL END)
    /COUNT(CASE WHEN t1.pageview_url="/products" THEN t1.website_session_id ELSE NULL END) AS pct_w_next_pg,
    
    COUNT(CASE WHEN t1.pageview_url="/the-original-mr-fuzzy" THEN t1.website_session_id ELSE NULL END) AS to_mrfuzzy,
    
    COUNT(CASE WHEN t1.pageview_url="/the-original-mr-fuzzy" THEN t1.website_session_id ELSE NULL END)
    /COUNT(CASE WHEN t1.pageview_url="/products" THEN t1.website_session_id ELSE NULL END) AS pct_to_mrfuzzy,
    
    COUNT(CASE WHEN t1.pageview_url="/the-forever-love-bear" THEN t1.website_session_id ELSE NULL END) AS to_lovebear,
    
    COUNT(CASE WHEN t1.pageview_url="/the-forever-love-bear" THEN t1.website_session_id ELSE NULL END)
    /COUNT(CASE WHEN t1.pageview_url="/products" THEN t1.website_session_id ELSE NULL END) AS pct_to_lovebear
FROM website_pageviews AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
WHERE t1.created_at BETWEEN "2012-10-06" AND "2013-04-06"
GROUP BY periods
