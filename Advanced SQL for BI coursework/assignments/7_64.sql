-- goal: session count column split by organic search, direct type in, paid brand search row split by month
-- all column categories as a percent of paid search nonbrand
-- organic search - http ref not null and utm source is null
-- direct type in - http ref is null
-- paid brand - utm source is not null and utm campaign is brand
-- paid nonbrand - utm source is not null and utm campaign is nonbrand
-- before dec 23rd

SELECT
	YEAR(created_at) AS yr,
    MONTH(created_at) AS mo,
    COUNT(CASE WHEN http_referer IS NOT NULL AND utm_campaign="nonbrand" THEN website_session_id ELSE NULL END) AS nonbrand,   
    COUNT(CASE WHEN http_referer IS NOT NULL AND utm_campaign="brand" THEN website_session_id ELSE NULL END) AS brand,
    
    COUNT(CASE WHEN http_referer IS NOT NULL AND utm_campaign="brand" THEN website_session_id ELSE NULL END)
    /COUNT(CASE WHEN http_referer IS NOT NULL AND utm_campaign="nonbrand" THEN website_session_id ELSE NULL END) AS brand_pct_of_nonbrand,
    
    COUNT(CASE WHEN http_referer IS NULL THEN website_session_id ELSE NULL END) AS direct_type_in,
    
	 COUNT(CASE WHEN http_referer IS NULL THEN website_session_id ELSE NULL END)
    /COUNT(CASE WHEN http_referer IS NOT NULL AND utm_campaign="nonbrand" THEN website_session_id ELSE NULL END) AS direct_pct_of_nonbrand,
    
    COUNT(CASE WHEN http_referer IS NOT NULL AND utm_source IS NULL THEN website_session_id ELSE NULL END) AS organic_search,

	COUNT(CASE WHEN http_referer IS NOT NULL AND utm_source IS NULL THEN website_session_id ELSE NULL END)
    /COUNT(CASE WHEN http_referer IS NOT NULL AND utm_campaign="nonbrand" THEN website_session_id ELSE NULL END) AS organic_pct_of_nonbrand

FROM website_sessions
WHERE created_At < "2012-12-23"
GROUP BY
	1,2