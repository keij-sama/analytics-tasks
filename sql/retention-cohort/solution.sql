WITH sessions AS (
    SELECT
        device_id,
        session_time::timestamptz::date AS session_date
    FROM retention_cohort
),
cohort AS (
    SELECT DISTINCT device_id
    FROM sessions
    WHERE session_date = DATE '2019-03-01'
),
cohort_activity AS (
    SELECT DISTINCT
        s.device_id,
        s.session_date
    FROM sessions AS s
    INNER JOIN cohort AS c
        ON c.device_id = s.device_id
    WHERE s.session_date BETWEEN DATE '2019-03-01' AND DATE '2019-03-07'
),
days AS (
    SELECT generate_series(0, 6) AS day_number
),
cohort_size AS (
    SELECT COUNT(*) AS users_count
    FROM cohort
)
SELECT
    d.day_number,
    DATE '2019-03-01' + d.day_number AS retention_date,
    COUNT(DISTINCT ca.device_id) AS retained_users,
    ROUND(
        100.0 * COUNT(DISTINCT ca.device_id) / NULLIF(cs.users_count, 0),
        2
    ) AS retention_rate_percent
FROM days AS d
CROSS JOIN cohort_size AS cs
LEFT JOIN cohort_activity AS ca
    ON ca.session_date = DATE '2019-03-01' + d.day_number
GROUP BY
    d.day_number,
    cs.users_count
ORDER BY d.day_number;
