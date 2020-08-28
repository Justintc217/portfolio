-- goal: user count by total number of sessions they had for all time
-- start of 2014 to nov 1st 2014
-- only consider users who began in this time frame
-- step 1: get users who began in 2014
-- step 2: determine number of sessions by user

WITH users_who_began_in_2014 AS (
SELECT
	DISTINCT user_id
FROM website_sessions
WHERE created_at BETWEEN "2014-01-01" AND "2014-11-01"
	AND is_repeat_session=0
),
repeats_by_user AS (
SELECT
	t1.user_id,
    SUM(is_repeat_session) AS repeats
FROM website_sessions AS t1
	INNER JOIN users_who_began_in_2014 AS t2
		ON t1.user_id = t2.user_id
WHERE created_at < "2014-11-01"
GROUP BY t1.user_id
)
SELECT
	repeats,
	COUNT(user_id) AS users
FROM repeats_by_user
GROUP BY repeats
ORDER BY repeats