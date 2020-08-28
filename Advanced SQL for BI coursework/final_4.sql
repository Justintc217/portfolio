-- goal session to order conv rate column split by channel and row split by quarter
-- direct type in - http is null, organic - utm source is null and http not null


SELECT
	MIN(DATE(t1.created_at)) AS quarter_start_date,
	MAX(DATE(t1.created_at)) AS quarter_end_date,
    
    COUNT(CASE WHEN t1.http_referer IS NULL THEN t2.order_id ELSE NULL END)
    /COUNT(CASE WHEN t1.http_referer IS NULL THEN t1.website_session_id ELSE NULL END) 
    AS direct_type_in_conv_rt,
    
    COUNT(CASE WHEN t1.http_referer IS NOT NULL AND t1.utm_source IS NULL THEN t2.order_id ELSE NULL END) 
    /COUNT(CASE WHEN t1.http_referer IS NOT NULL AND t1.utm_source IS NULL THEN t1.website_session_id ELSE NULL END) 
    AS organic_search_conv_rt,
    
    COUNT(CASE WHEN t1.utm_source="gsearch" AND utm_campaign="nonbrand" THEN t2.order_id ELSE NULL END) 
    /COUNT(CASE WHEN t1.utm_source="gsearch" AND utm_campaign="nonbrand" THEN t1.website_session_id ELSE NULL END) 
    AS gsearch_nonbrand_conv_rt,    
    
    COUNT(CASE WHEN t1.utm_source="bsearch" AND utm_campaign="nonbrand" THEN t2.order_id ELSE NULL END) 
    /COUNT(CASE WHEN t1.utm_source="bsearch" AND utm_campaign="nonbrand" THEN t1.website_session_id ELSE NULL END) 
    AS bsearch_nonbrand_conv_rt,    
    
    COUNT(CASE WHEN utm_campaign="brand" THEN t2.order_id ELSE NULL END)
    /COUNT(CASE WHEN utm_campaign="brand" THEN t1.website_session_id ELSE NULL END) 
    AS brand_conv_rt,
    CASE WHEN TIMESTAMPDIFF(
		QUARTER, 
		MIN(DATE(t1.created_at)),
		MAX(DATE_ADD(t1.created_at, INTERVAL 1 DAY))
    ) = 1 THEN "full quarter" ELSE "partial quarter" END AS is_full_quarter
FROM website_sessions AS t1
	LEFT JOIN orders AS t2
		ON t1.website_session_id = t2.website_session_id
GROUP BY
	YEAR(t1.created_at),
	quarter(t1.created_at)