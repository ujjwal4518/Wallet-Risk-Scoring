import os
import pandas as pd
from src.fetch_data import fetch_wallet_data
from src.feature_engineering import create_features
from src.scoring import assign_scores

def main():
    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # Read wallet addresses
    wallets = pd.read_csv("data/wallets.csv")["wallet_id"].tolist()

    # Fetch raw data from Compound V2
    print("Fetching wallet data...")
    raw_df = fetch_wallet_data(wallets)

    # Show a preview of raw data
    print("\n Raw Data Preview:")
    print(raw_df.head())
    print(raw_df.columns)

    # Feature engineering
    print("\n Engineering features...")
    features_df = create_features(raw_df)

    # Show feature summary
    print("\n Feature Stats:")
    print(features_df[["borrow_supply_ratio", "activity_score"]].describe())

    # Risk scoring
    print("\n Assigning risk scores...")
    scores_df = assign_scores(features_df)

    # Save results
    output_path = "output/risk_scores.csv"
    scores_df.to_csv(output_path, index=False)
    print(f"\n Risk scores saved to {output_path}")

if __name__ == "__main__":
    main()
