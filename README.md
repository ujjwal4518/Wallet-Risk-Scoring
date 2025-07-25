# 🛡️ Wallet Risk Scoring From Scratch

## 📄 Overview

This project evaluates the on-chain lending behavior of 100 Ethereum wallets and assigns each a **risk score from 0 to 1000**, using on-chain transaction data from **Compound V2 and Compound V3** protocols.

---

## 📦 Data Collection

- Data was fetched using **The Graph's hosted subgraphs**:
  - Compound V2: [`graphprotocol/compound-v2`](https://thegraph.com/hosted-service/subgraph/graphprotocol/compound-v2)
  - Compound V3 (Ethereum): [`0xgens/compound-v3-ethereum`](https://api.thegraph.com/subgraphs/name/0xgens/compound-v3-ethereum)
- Each wallet address was queried for:
  - **Supply and borrow transactions**
  - Total borrow/supply amounts
  - Number of interactions

---

## ⚙️ Feature Engineering

The following features were extracted to reflect each wallet’s financial behavior:

| Feature               | Description                            |
| --------------------- | -------------------------------------- |
| `total_borrow`        | Sum of all borrow amounts              |
| `total_supply`        | Sum of all supply amounts              |
| `borrow_count`        | Number of borrow transactions          |
| `supply_count`        | Number of supply transactions          |
| `borrow_supply_ratio` | `total_borrow / (total_supply + 1e-6)` |
| `activity_score`      | `borrow_count + supply_count`          |

---

## 🧠 Risk Scoring Logic

Each wallet is scored on a **0–1000** scale based on the above features:

1. **Normalize features** using MinMaxScaler.
2. **Risk formula**:
   ```python
   risk = 0.7 * borrow_supply_ratio + 0.3 * (1 - normalized_activity)
   score = 1000 * (1 - risk)
   ```
