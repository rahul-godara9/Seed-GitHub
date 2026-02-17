
-- Build simple user-level features:
-- - total_spend_30d
-- - txn_count_30d
-- - avg_order_value
-- - recency_days (since last txn)
-- - sessions_last_7d (web events count)
-- - first_signup_week (derived from signup_date)

-- Set "today" for reproducibility. Replace with CURRENT_DATE on RDBMS that supports it.
WITH params AS (
    SELECT DATE('2025-06-10') AS as_of_date
),

txns_30d AS (
    SELECT
        t.user_id,
        SUM(t.amount) AS total_spend_30d,
        COUNT(*) AS txn_count_30d,
        CASE WHEN COUNT(*) = 0 THEN 0 ELSE SUM(t.amount) * 1.0 / COUNT(*) END AS avg_order_value,
        MAX(DATE(t.txn_timestamp)) AS last_txn_date
    FROM transactions t
    JOIN params p
      ON DATE(t.txn_timestamp) BETWEEN DATE(p.as_of_date, '-30 day') AND p.as_of_date
    GROUP BY t.user_id
),

recency AS (
    SELECT
        u.user_id,
        CASE
            WHEN x.last_txn_date IS NULL THEN NULL
            ELSE CAST((JULIANDAY((SELECT as_of_date FROM params)) - JULIANDAY(x.last_txn_date)) AS INTEGER)
        END AS recency_days
    FROM users u
    LEFT JOIN txns_30d x ON u.user_id = x.user_id
),

sessions_7d AS (
    SELECT
        w.user_id,
        COUNT(*) AS sessions_last_7d
    FROM web_events w
    JOIN params p
      ON DATE(w.event_timestamp) BETWEEN DATE(p.as_of_date, '-7 day') AND p.as_of_date
    GROUP BY w.user_id
),

signup_feats AS (
    SELECT
        u.user_id,
        STRFTIME('%Y-%W', u.signup_date) AS first_signup_week
    FROM users u
)

-- Final features result
SELECT
    u.user_id,
    u.user_name,
    u.country,
    COALESCE(x.total_spend_30d, 0) AS total_spend_30d,
    COALESCE(x.txn_count_30d, 0)   AS txn_count_30d,
    COALESCE(x.avg_order_value, 0) AS avg_order_value,
    r.recency_days,
    COALESCE(s.sessions_last_7d, 0) AS sessions_last_7d,
    sf.first_signup_week
FROM users u
LEFT JOIN txns_30d x    ON u.user_id = x.user_id
LEFT JOIN recency r     ON u.user_id = r.user_id
LEFT JOIN sessions_7d s ON u.user_id = s.user_id
LEFT JOIN signup_feats sf ON u.user_id = sf.user_id
ORDER BY u.user_id;
