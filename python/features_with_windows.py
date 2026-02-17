
"""
Window-function-style features (pandas equivalent):
- rolling 30-day spend per user (daily)
- trailing 3-transaction average
Outputs per-user daily rollups and a final snapshot for AS_OF_DATE.
"""

import pandas as pd
from utils_io import maybe_create_mock_data, load_data

AS_OF_DATE = pd.Timestamp("2024-07-28")
## changed date to test conflict

def main():
    maybe_create_mock_data()
    users, txns, _ = load_data()

    # Ensure timestamps are at daily granularity
    txns["date"] = txns["txn_timestamp"].dt.date
    txns["date"] = pd.to_datetime(txns["date"])

    # Build a daily date range per user to allow rolling windows with missing dates
    all_dates = pd.DataFrame({"date": pd.date_range(txns["date"].min(), AS_OF_DATE, freq="D")})
    per_user = []
    for uid, g in txns.groupby("user_id"):
        # daily amount
        daily = g.groupby("date")["amount"].sum().reset_index()
        daily = all_dates.merge(daily, on="date", how="left").fillna({"amount": 0})
        daily["user_id"] = uid

        # 30-day rolling sum
        daily = daily.sort_values(["user_id", "date"]).reset_index(drop=True)
        daily["rolling_spend_30d"] = daily["amount"].rolling(window=30, min_periods=1).sum()
        per_user.append(daily)

    daily_rollups = pd.concat(per_user, ignore_index=True)

    # Trailing 3-transaction average (by txn order)
    txns = txns.sort_values(["user_id", "txn_timestamp"]) 
    txns["t3_avg"] = txns.groupby("user_id")["amount"].rolling(3, min_periods=1).mean().reset_index(level=0, drop=True)

    # Snapshot of features at AS_OF_DATE
    snapshot = daily_rollups[daily_rollups["date"] == AS_OF_DATE]
    snapshot = snapshot.merge(users[["user_id", "user_name"]], on="user_id", how="left")
    snapshot = snapshot[["user_id", "user_name", "rolling_spend_30d"]].sort_values("user_id")

    daily_rollups.to_csv("user_daily_rollups.csv", index=False)
    txns.to_csv("transactions_with_t3avg.csv", index=False)
    snapshot.to_csv("user_features_windows_snapshot.csv", index=False)

    print("Wrote user_daily_rollups.csv, transactions_with_t3avg.csv, user_features_windows_snapshot.csv")
    print(snapshot)

if __name__ == "__main__":
    main()
