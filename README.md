# IB Historical Data Downloader

Simple Python script for downloading **historical market data from Interactive Brokers**
for **multiple tickers and multiple timeframes**, saved as **standard CSV files**.

Supports stocks/ETFs (e.g. `GLD`) and indexes (e.g. `VIX`).

---

## Requirements

- Python **3.9+**
- Interactive Brokers **TWS or IB Gateway**
- IB **Paper Trading** or Live account
- `ibapi` (official IB Python API)

---

## Installation

1. **Install Python packages**
   ```bash
   pip install --upgrade ibapi
Start IB Gateway or TWS

Paper trading gateway default port: 4002

TWS paper trading port: 7497

Enable API access in IB

Settings → API → Enable ActiveX and Socket Clients

Disable “Read-Only API” (if enabled)

Configuration
Edit the USER AREA in ib_hist.py:

python
Copy code
TICKERS = ["GLD", "VIX"]

TIMEFRAMES = {
    "1min": "1 min",
    "5min": "5 mins",
    "15min": "15 mins",
    "1hour": "1 hour",
    "1day": "1 day"
}
Note: Some instruments (e.g. VIX) do not support minute bars in IB.

Run
bash
Copy code
python ib_hist.py
CSV files will be saved to:

Copy code
historical_data/
Output Format
Standard CSV:

csv
Copy code
Date,Open,High,Low,Close,Volume
20240102 09:30,187.1,187.6,186.9,187.4,123456
Compatible with Excel, Pandas, TradingView, etc.

Common Notes
IB prints many warnings (2104 / 2106 / 2176).
These are normal and do not block historical data.

Indexes (e.g. VIX) must be requested as IND on CBOE.

IB limits historical duration for small bar sizes (1–5 min).

Disclaimer
For educational and research purposes only.
Not financial advice.
