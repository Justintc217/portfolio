-- goal find min,max,and avg days between first and second session for users who began in 2014
-- before nov 3rd
-- step 1: get users who began in 2014 and datetime of their sessions
-- step 2: get users first and second session then get the datediff between them
-- second session can be the earliest repeat session

WITH user_first_two_sessions AS (
SELECT
	user_id,
    MIN(CASE WHEN is_repeat_session=0 THEN created_at ELSE NULL END) AS first_session,
    MIN(CASE WHEN is_repeat_session=1 THEN created_at ELSE NULL END) AS second_session
FROM website_sessions
WHERE created_at BETWEEN "2014-01-01" AND "2014-11-03"
GROUP BY user_id
HAVING first_session IS NOT NULL AND second_session IS NOT NULL
)
SELECT
	MAX(datediff(second_session, first_session)) AS max_days_first_to_second,
	MIN(datediff(second_session, first_session)) AS min_days_first_to_second,
	AVG(datediff(second_session, first_session)) AS avg_days_first_to_second
FROM user_first_two_sessions

