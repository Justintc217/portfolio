-- goal: nonbrand weekly sessions column split by b/gsearch and device
-- also get bsearch as a percent of gsearch split by device
-- BETWEEN "2012-11-04" AND "2012-12-22"
-- nonbrand filter
USE mavenfuzzyfactory;

SELECT
	DATE(MIN(created_at)) AS week_start_date,
    COUNT(CASE WHEN utm_source="gsearch" AND device_type="desktop" 
    THEN website_session_id ELSE NULL END) AS g_dtop_sessions,
    COUNT(CASE WHEN utm_source="bsearch" AND device_type="desktop" 
    THEN website_session_id ELSE NULL END) AS b_dtop_sessions,
    
    COUNT(CASE WHEN utm_source="bsearch" AND device_type="desktop" THEN website_session_id ELSE NULL END) 
    / COUNT(CASE WHEN utm_source="gsearch" AND device_type="desktop" 
    THEN website_session_id ELSE NULL END) AS b_pct_of_g_dtop,
    
    COUNT(CASE WHEN utm_source="gsearch" AND device_type="mobile" 
    THEN website_session_id ELSE NULL END) AS g_mob_sessions,
    COUNT(CASE WHEN utm_source="bsearch" AND device_type="mobile" 
    THEN website_session_id ELSE NULL END) AS b_mob_sessions,
    
	COUNT(CASE WHEN utm_source="bsearch" AND device_type="mobile" THEN website_session_id ELSE NULL END) 
    / COUNT(CASE WHEN utm_source="gsearch" AND device_type="mobile" 
    THEN website_session_id ELSE NULL END) AS b_pct_of_g_mob
FROM website_sessions
WHERE created_at BETWEEN "2012-11-04" AND "2012-12-22"
	AND utm_campaign="nonbrand"
GROUP BY
	WEEK(created_at)