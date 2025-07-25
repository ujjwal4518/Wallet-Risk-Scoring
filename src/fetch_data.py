import requests
import pandas as pd
from tqdm import tqdm

# Compound V3 Subgraph (Ethereum)
GRAPH_URL = "https://api.thegraph.com/subgraphs/name/0xgens/compound-v3-ethereum"

def query_subgraph(wallet):
    query = """
    {
      account(id: "%s") {
        id
        supplies {
          asset {
            symbol
          }
          amount
        }
        borrows {
          asset {
            symbol
          }
          amount
        }
      }
    }
    """ % wallet.lower()

    response = requests.post(GRAPH_URL, json={'query': query})
    return response.json()

def fetch_wallet_data(wallets):
    results = []

    for wallet in tqdm(wallets):
        data = query_subgraph(wallet)
        account = data.get("data", {}).get("account")

        if not account:
            results.append({
                "wallet_id": wallet,
                "total_borrow": 0.0,
                "total_supply": 0.0,
                "borrow_count": 0,
                "supply_count": 0
            })
            continue

        total_borrow = sum(float(b["amount"]) for b in account.get("borrows", []))
        total_supply = sum(float(s["amount"]) for s in account.get("supplies", []))

        results.append({
            "wallet_id": wallet,
            "total_borrow": total_borrow,
            "total_supply": total_supply,
            "borrow_count": len(account.get("borrows", [])),
            "supply_count": len(account.get("supplies", []))
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    wallets_df = pd.read_csv("data/wallets.csv")
    df = fetch_wallet_data(wallets_df["wallet_id"].tolist())
    df.to_csv("output/raw_data.csv", index=False)
