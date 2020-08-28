-- goal: percent of traffic from mobile split by gsearch and bsearch (
-- nonbrand only
-- "2012-08-22" AND "2012-11-30"
-- step 1: mobile sessions / desktop sessions

SELECT
	utm_source,
    COUNT(website_session_id) AS sessions,
    COUNT(CASE WHEN device_type="mobile" THEN website_session_id ELSE NULL END) AS mobile_sessions,
    CONCAT(
		TRUNCATE(
			100 * COUNT(CASE WHEN device_type="mobile" THEN website_session_id ELSE NULL END)/
			COUNT(website_session_id), 2
            ), "%"
        ) AS pct_mobile
FROM website_sessions
WHERE utm_campaign="nonbrand"
	AND created_at BETWEEN "2012-08-22" AND "2012-11-30"
GROUP BY utm_source
ORDER BY utm_source


