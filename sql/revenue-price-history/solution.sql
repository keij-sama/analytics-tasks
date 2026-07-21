SELECT
    SUM(
        CASE t.action
            WHEN 'purchase' THEN ph.price
            WHEN 'refund' THEN -ph.price
            ELSE 0
        END
    ) AS total_revenue
FROM transactions AS t
INNER JOIN price_history AS ph
    ON ph.item_id = t.item_id
   AND t.event_timestamp >= ph.valid_from
   AND (
       t.event_timestamp < ph.valid_to
       OR ph.valid_to IS NULL
   );
