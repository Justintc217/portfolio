SELECT
	utm_source,
    utm_campaign,
    http_referer,
    COUNT(website_session_id) AS sessions
FROM
	website_sessions
WHERE
	created_at < "2012-04-12"
GROUP BY
	utm_source,
    utm_campaign,
    http_referer
ORDER BY sessions DESC;

















jdbc:mysql://127.0.0.1:3306/?user=root
