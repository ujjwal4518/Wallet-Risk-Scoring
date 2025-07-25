import pandas as pd

def create_features(df):
    df["borrow_supply_ratio"] = df["total_borrow"] / (df["total_supply"] + 1e-6)
    df["activity_score"] = df["borrow_count"] + df["supply_count"]
    df.fillna(0, inplace=True)
    return df
