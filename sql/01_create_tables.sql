
-- Create minimal tables for demo feature creation

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS web_events;

CREATE TABLE users (
    user_id        INTEGER PRIMARY KEY,
    user_name      VARCHAR(50),
    country        VARCHAR(50),
    signup_date    DATE
);

CREATE TABLE transactions (
    txn_id         INTEGER PRIMARY KEY,
    user_id        INTEGER,
    amount         DECIMAL(10,2),
    currency       VARCHAR(10),
    txn_timestamp  TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE web_events (
    event_id        INTEGER PRIMARY KEY,
    user_id         INTEGER,
    event_type      VARCHAR(50),
    event_timestamp TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
