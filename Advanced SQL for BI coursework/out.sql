USE mavenfuzzyfactory;

SELECT
	DATE(MIN(created_at)) AS week_start_date,
	device_type,
    utm_source,
    COUNT(website_session_id) AS sessions
FROM website_sessions
WHERE created_at BETWEEN "2012-11-04" AND "2012-12-22"
	AND utm_campaign="nonbrand"
    AND utm_source IN ("gsearch","bsearch")
GROUP BY
	WEEK(created_at),
    device_type,
    utm_source
ORDER BY
	WEEK(created_at),
    device_type,
    utm_source