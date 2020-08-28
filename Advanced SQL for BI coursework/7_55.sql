-- goal: weekly session volume of gsearch nonbrand and bsearch
-- began on "2012-08-22" (as of "2012-11-29")
-- nonbrand for both

SELECT
	MIN(DATE(created_at)) AS week_start_date,
    COUNT(website_session_id) AS total_sessions,
    COUNT(CASE WHEN utm_source="gsearch"
    THEN website_session_id ELSE NULL END) AS gsearch_sessions,
    COUNT(CASE WHEN utm_source="bsearch" 
    THEN website_session_id ELSE NULL END) AS bsearch_sessions
FROM website_sessions
WHERE created_at BETWEEN "2012-08-22" AND "2012-11-29"
	AND utm_campaign="nonbrand"
GROUP BY 
	WEEK(created_at)