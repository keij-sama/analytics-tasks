WITH prepared AS (
    SELECT
        card_number,
        date_trunc(
            'month',
            to_timestamp(sale_dttm, 'DD/MM/YYYY HH24:MI')
        )::date AS sale_month,
        price * (1 - discount / 100.0) AS net_amount
    FROM coffee_sales
),
months_count AS (
    SELECT COUNT(DISTINCT sale_month) AS value
    FROM prepared
),
regular_clients AS (
    SELECT card_number
    FROM prepared
    GROUP BY card_number
    HAVING COUNT(DISTINCT sale_month) = (SELECT value FROM months_count)
),
monthly_client_spend AS (
    SELECT
        p.sale_month,
        p.card_number,
        SUM(p.net_amount) AS monthly_spend
    FROM prepared AS p
    INNER JOIN regular_clients AS rc
        ON rc.card_number = p.card_number
    GROUP BY
        p.sale_month,
        p.card_number
),
ranked AS (
    SELECT
        sale_month,
        monthly_spend,
        ROW_NUMBER() OVER (
            PARTITION BY sale_month
            ORDER BY monthly_spend
        ) AS row_number,
        COUNT(*) OVER (
            PARTITION BY sale_month
        ) AS rows_count
    FROM monthly_client_spend
)
SELECT
    sale_month,
    ROUND(AVG(monthly_spend), 2) AS median_monthly_spend
FROM ranked
WHERE row_number IN (
    (rows_count + 1) / 2,
    (rows_count + 2) / 2
)
GROUP BY sale_month
ORDER BY sale_month;
