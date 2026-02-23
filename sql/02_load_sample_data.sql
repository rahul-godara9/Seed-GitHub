
-- Insert small, readable sample rows

INSERT INTO users (user_id, user_name, country, signup_date) VALUES
(1, 'Asha', 'IN', DATE('2024-02-01')),
(2, 'Ben',  'US', DATE('2024-02-15')),
(3, 'Chen', 'SG', DATE('2024-03-10'));

INSERT INTO transactions (txn_id, user_id, amount, currency, txn_timestamp) VALUES
(101, 1, 120.00, 'INR', DATETIME('2024-05-01 10:00:00')),
(102, 1,  80.50, 'INR', DATETIME('2024-05-28 12:30:00')),
(103, 2,  50.00, 'USD', DATETIME('2024-05-15 08:10:00')),
(104, 2,  75.00, 'USD', DATETIME('2024-06-01 14:45:00')),
(105, 3,  30.00, 'SGD', DATETIME('2024-06-02 16:20:00'));

INSERT INTO web_events (event_id, user_id, event_type, event_timestamp) VALUES
(201, 1, 'page_view',   DATETIME('2024-05-27 09:00:00')),
(202, 1, 'add_to_cart', DATETIME('2024-05-28 09:15:00')),
(203, 2, 'page_view',   DATETIME('2024-05-30 10:00:00')),
(204, 2, 'checkout',    DATETIME('2024-06-01 14:00:00')),
(205, 3, 'page_view',   DATETIME('2024-06-02 16:00:00'));

-- Note: For Postgres, replace DATE('YYYY-MM-DD') with DATE 'YYYY-MM-DD' and
-- DATETIME with TIMESTAMP 'YYYY-MM-DD HH24:MI:SS'.
