-- goal: new sessions and repeat sessions row split by channel group
-- Q: repeat sessions are counted once per user or for every repeat session
-- Q: only for users that began in 2014 or repeat sessions for any user who began at anytime?
-- channels...
-- organic search - http ref not null and utm source is null
-- direct type in - http ref is null
-- paid brand - utm source is not null and utm campaign is brand
-- paid nonbrand - utm source is not null and utm campaign is nonbrand
-- social - utm source is socialbook

WITH users_2014 AS (
SELECT
	DISTINCT user_id
FROM website_sessions
WHERE created_at BETWEEN "2014-01-01" AND "2014-11-05"
-- 	AND is_repeat_session=0 #depends on if you want 2014-start users only
)
SELECT
	CASE
		WHEN http_referer IS NOT NULL AND utm_source IS NULL THEN "organic search"
		WHEN http_referer IS NULL THEN "direct type in"
		WHEN utm_source IS NOT NULL AND utm_campaign="brand" THEN "paid brand"
		WHEN utm_source IS NOT NULL AND utm_campaign="nonbrand" THEN "paid nonbrand"
        WHEN utm_source="socialbook" THEN "paid_social"
        ELSE "uh oh..."
	END AS channel_group,
    COUNT(CASE WHEN is_repeat_session=0 THEN website_sessions.user_id ELSE NULL END) AS new_sessions,
    COUNT(CASE WHEN is_repeat_session=1 THEN website_sessions.user_id ELSE NULL END) AS repeat_sessions
FROM website_sessions
	INNER JOIN users_2014
		ON users_2014.user_id = website_sessions.user_id
WHERE created_at BETWEEN "2014-01-01" AND "2014-11-05"
GROUP BY channel_group