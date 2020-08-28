def get_landing_pages(start, end):
    out = (
        f"""
SELECT
    pageview_url,
    MIN(website_pageview_id) AS first_pageview,
    COUNT(website_pageview_id) AS pageviews
FROM website_pageviews
    INNER JOIN website_sessions
        ON website_pageviews.website_session_id = website_sessions.website_session_id
WHERE website_pageviews.created_at BETWEEN '{start}' AND '{end}'
    AND utm_source = 'gsearch'
    AND utm_campaign = 'nonbrand'
GROUP BY website_sessions.website_session_id"""
    )
    return out


def bounces(pageviews):
    return f"COUNT(CASE WHEN {pageviews} = 1 THEN {pageviews} ELSE NULL END)"
