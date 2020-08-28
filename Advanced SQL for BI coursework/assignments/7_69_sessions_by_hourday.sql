-- goal: avg session volume row split by hour and column split by day of week ( use name)
-- average is count of instances with granulatiry of hour of day divided by number of occurances between sep 15 and nov 15




WITH sessions_by_hourday AS (
SELECT
	DATE(created_at) AS date,
	DAYNAME(created_at) AS day_of_week,
    HOUR(created_at) AS hour,
	COUNT(website_session_id) AS sessions
FROM website_sessions
WHERE created_at BETWEEN "2012-09-15" AND "2012-11-15"
GROUP BY
	1,2,3
)
SELECT
	day_of_week,
    hour,
	AVG(sessions)
FROM sessions_by_hourday
GROUP BY
	WEEKDAY(date),2
ORDER BY
	WEEKDAY(date),2