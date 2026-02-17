
"""
Compute simple user-level features from CSVs using pandas:
- total_spend_30d
- txn_count_30d
- avg_order_value
- sessions_last_7d
- recency_days (days since last txn)
- first_signup_week (YYYY-WW)
"""

import pandas as pd
from utils_io import maybe_create_mock_data, load_data

AS_OF_DATE = pd.Timestamp("2024-06-03")  # fixed for demo


## adding a comment for the test ## HC-2026-02-17
def main():
    # Generate CSVs the first time you run the script
    maybe_create_mock_data()

    users, txns, events = load_data()

    # 30-day window for transactions
    start_30d = AS_OF_DATE - pd.Timedelta(days=30)
    txns_30d = txns[(txns["txn_timestamp"] >= start_30d) & (txns["txn_timestamp"] <= AS_OF_DATE)]

    agg_txn = txns_30d.groupby("user_id").agg(
        total_spend_30d=("amount", "sum"),
        txn_count_30d=("txn_id", "count"),
        last_txn_date=("txn_timestamp", "max"),
    ).reset_index()

    agg_txn["avg_order_value"] = agg_txn["total_spend_30d"] / agg_txn["txn_count_30d"]
    # Fill NA for users with no txns in window
    agg_txn = agg_txn.fillna({"total_spend_30d": 0.0, "txn_count_30d": 0, "avg_order_value": 0.0})

    # recency_days
    agg_txn["recency_days"] = (AS_OF_DATE - agg_txn["last_txn_date"]).dt.days
    agg_txn.loc[agg_txn["last_txn_date"].isna(), "recency_days"] = None

    # 7-day window for sessions (web events)
    start_7d = AS_OF_DATE - pd.Timedelta(days=7)
    events_7d = events[(events["event_timestamp"] >= start_7d) & (events["event_timestamp"] <= AS_OF_DATE)]
    sessions = events_7d.groupby("user_id").size().reset_index(name="sessions_last_7d")

    # signup week
    users["first_signup_week"] = users["signup_date"].dt.strftime("%Y-%W")

    # Join all features
    feats = users.merge(agg_txn.drop(columns=["last_txn_date"]), on="user_id", how="left")                  .merge(sessions, on="user_id", how="left")

    feats = feats.fillna({"total_spend_30d": 0.0, "txn_count_30d": 0, "avg_order_value": 0.0, "sessions_last_7d": 0})
    feats = feats[[
        "user_id", "user_name", "country",
        "total_spend_30d", "txn_count_30d", "avg_order_value",
        "recency_days", "sessions_last_7d", "first_signup_week"
    ]].sort_values("user_id")

    feats.to_csv("user_features_basic.csv", index=False)
    print("Wrote user_features_basic.csv")
    print(feats)

if __name__ == "__main__":
    main()
