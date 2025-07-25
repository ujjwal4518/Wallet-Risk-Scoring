from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

def assign_scores(df):
    # Fix future pandas warning
    df["borrow_supply_ratio"] = df["borrow_supply_ratio"].replace([np.inf, -np.inf], 0)
    df.fillna(0, inplace=True)

    # Filter features
    features = df[["borrow_supply_ratio", "activity_score"]].copy()
    features["activity_score"] = features["activity_score"].replace(0, 0.01)

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(features)

    # Weighted score with noise
    risk_raw = 0.7 * scaled[:, 0] + 0.3 * (1 - scaled[:, 1])
    noise = np.random.normal(0, 0.01, len(risk_raw))
    final_risk = np.clip(risk_raw + noise, 0, 1)

    df["score"] = (1000 * (1 - final_risk)).astype(int)
    return df[["wallet_id", "score"]]
