
"""
Tiny I/O helpers to create/load mock CSVs for the feature scripts.
"""

import pandas as pd

def maybe_create_mock_data():
    # Users
    users = pd.DataFrame([
        {"user_id": 1, "user_name": "Asha", "country": "IN", "signup_date": "2024-01-01"},
        {"user_id": 2, "user_name": "Ben",  "country": "US", "signup_date": "2024-02-15"},
        {"user_id": 3, "user_name": "Chen", "country": "SG", "signup_date": "2024-03-10"},
    ])
    users.to_csv("users.csv", index=False)

    # Transactions
    transactions = pd.DataFrame([
        {"txn_id": 101, "user_id": 1, "amount": 120.00, "currency": "INR", "txn_timestamp": "2024-05-01 10:00:00"},
        {"txn_id": 102, "user_id": 1, "amount":  80.50, "currency": "INR", "txn_timestamp": "2024-05-28 12:30:00"},
        {"txn_id": 103, "user_id": 2, "amount":  50.00, "currency": "USD", "txn_timestamp": "2024-05-15 08:10:00"},
        {"txn_id": 104, "user_id": 2, "amount":  75.00, "currency": "USD", "txn_timestamp": "2024-06-01 14:45:00"},
        {"txn_id": 105, "user_id": 3, "amount":  30.00, "currency": "SGD", "txn_timestamp": "2024-06-02 16:20:00"},
    ])
    transactions.to_csv("transactions.csv", index=False)

    # Web events
    web_events = pd.DataFrame([
        {"event_id": 201, "user_id": 1, "event_type": "page_view",   "event_timestamp": "2024-05-27 09:00:00"},
        {"event_id": 202, "user_id": 1, "event_type": "add_to_cart", "event_timestamp": "2024-05-28 09:15:00"},
        {"event_id": 203, "user_id": 2, "event_type": "page_view",   "event_timestamp": "2024-05-30 10:00:00"},
        {"event_id": 204, "user_id": 2, "event_type": "checkout",    "event_timestamp": "2024-06-01 14:00:00"},
        {"event_id": 205, "user_id": 3, "event_type": "page_view",   "event_timestamp": "2024-06-02 16:00:00"},
    ])
    web_events.to_csv("web_events.csv", index=False)


def load_data():
    users = pd.read_csv("users.csv", parse_dates=["signup_date"])
    txns = pd.read_csv("transactions.csv", parse_dates=["txn_timestamp"])
    events = pd.read_csv("web_events.csv", parse_dates=["event_timestamp"])
    return users, txns, events
