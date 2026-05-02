# 📊 Stablecoin Intelligence Dashboard

 A real-time monitoring platform that tracks 180+ stablecoins, calculates risk metrics, and visualizes market health using live CoinGecko data.



![Dashboard Preview](assets/stablecoin%20intelligence%20dashboards.png)





## 🎯 What Problem Does This Solve?

The stablecoin market moves fast. Depegging events, liquidity crises, and supply shocks can happen within minutes. This dashboard gives analysts and traders a single view of the entire stablecoin market — showing which coins are healthy, which are at risk, and why.



##  Live Features

- 🔴 **Real-time monitoring** of 180+ stablecoins every 5 minutes
- 📉 **Depeg detection** with low, medium and critical severity alerts
- ⚠️ **Stress Index** — composite risk score combining 7 metrics
- 💧 **Liquidity tracking** across the entire stablecoin market
- 🔄 **Supply change monitoring** — detects minting and burning activity
- 📊 **Interactive charts** — heatmap, waterfall, funnel, area and donut
- 📥 **CSV export** of any filtered dataset
- ⏰ **Automated pipeline** via Apache Airflow every 5 minutes



## 📐 Architecture

CoinGecko API
│
│  250+ stablecoins raw JSON
▼
Extract ──────────────────▶ data/raw/
│                        JSON backup
│  raw data
▼
Transform
│  cleans + calculates
│  7 metrics per coin
▼
Validate
│  removes invalid
│  coins and outliers
├──────────────────────▶ data/processed/
│                        CSV backup
│  140+ valid coins
▼
PostgreSQL
│  5 tables updated
│  every 5 minutes
▼
Streamlit
│  reads latest data
│  renders charts
▼
Browser
Dashboard


---

## 📊 Metrics

| Metric | Formula | What It Tells You |
|--------|---------|-------------------|
| **Depeg Score** | `\|price - 1.00\| / 1.00 * 100` | How far coin is from $1.00 peg |
| **Market Share** | `market_cap / total_market_cap * 100` | Dominance in stablecoin market |
| **Velocity** | `volume / market_cap` | How actively the coin is being used |
| **Liquidity Ratio** | `volume / circulating_supply` | Ease of buying and selling |
| **Utilization** | `circulating_supply / total_supply * 100` | Supply being actively used |
| **Supply Change** | `circulating_supply * price_change_24h` | Minting or burning activity |
| **Stress Index** | `weighted(depeg + liquidity + utilization)` | Overall risk score 0-100 |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Data Source | CoinGecko API |
| Language | Python 3.10+ |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy |
| Orchestration | Apache Airflow |
| Dashboard | Streamlit |
| Charts | Plotly |
| Data Processing | Pandas |
| Containerization | Docker |

---

## 📁 Project Structure

STABLECOIN-TRACKER/
├── app/
│   └── dashboard.py          # Streamlit dashboard
├── config/
│   └── setting.py           # All configuration
├── dags/
│   └── stablecoin_pipeline.py # Airflow DAG
├── src/
│   ├── api/                  # CoinGecko client
│   ├── database/             # Models and connection
│   ├── metrics/              # 7 metric calculators
│   ├── pipeline/             # ETL pipeline
│   └── utils/                # Logger and helpers
├── main.py                   # Pipeline entry point
└── app.py

---

🔍 Key Insights
    Which stablecoins are at risk of depegging right now
    Which coins dominate the stablecoin market
    Where liquidity is concentrated across the market
    Which coins are minting or burning supply aggressively
    Composite risk ranking of every tracked stablecoin

🗄️ Database
Five PostgreSQL tables store all metrics:
    stablecoin_prices   → price, depeg_score, market_cap
    supply_metrics      → total_supply, market_share
    activity_metrics    → velocity, utilization, volume
    liquidity_metrics   → liquidity_ratio, pool_depth
    risk_metrics        → stress_index, depeg_score


## ⚡ Quick Start

**1. Clone and install**
```bash
git clone https://github.com/Ranky13/stablecoin-tracker
cd stablecoin-tracker
pip install -r requirements.txt


📄 License
MIT License — free to use for learning and portfolio purposes.