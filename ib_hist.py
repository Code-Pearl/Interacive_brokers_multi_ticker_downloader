"""
IBAPI - Getting historical data (multiple tickers, multiple timeframes)

pip install --upgrade ibapi
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import os
import csv

class TradingApp(EWrapper, EClient):
   
    def __init__(self):
        EClient.__init__(self,self)
        self.data_received = threading.Event()
        self.data_store = {}

    def historicalData(self, reqId, bar):
        if reqId not in self.data_store:
            self.data_store[reqId] = []

        self.data_store[reqId].append([
            bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume
        ])

    def historicalDataEnd(self, reqId, start, end):
        self.data_received.set()

    def error(self, reqId, errorCode, errorString):
        print(f"ERROR {reqId} {errorCode} {errorString}")

def websocket_con():
    app.run()


app = TradingApp()
app.connect("127.0.0.1", 4002, clientId=0)

threading.Thread(target=websocket_con, daemon=True).start()
time.sleep(1)

def security(symbol, sec_type="STK", currency="USD", exchange="SMART"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract
"""

    if symbol == "VIX":
        contract.secType = "IND"
        contract.exchange = "CBOE"
        
        
"""


def histData(req_num, contract, duration, candle_size):
    app.data_received.clear()

    app.reqHistoricalData(
        reqId=req_num,
        contract=contract,
endDateTime=time.strftime("%Y%m%d-%H:%M:%S"),
        durationStr=duration,
        barSizeSetting=candle_size,
        whatToShow='TRADES',
        useRTH=1,
        formatDate=1,
        keepUpToDate=0,
        chartOptions=[]
    )

    if not app.data_received.wait(timeout=60):
        print(f"Timeout for request {req_num}")

def save_to_csv(data, filename):
    os.makedirs("historical_data", exist_ok=True)
    filepath = os.path.join("historical_data", filename)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date","Open","High","Low","Close","Volume"])
        writer.writerows(data)

# ===================== USER AREA =====================

TICKERS = ["GLD", "TQQQ"]

TIMEFRAMES = {
    "1min": "1 min",
    "5min": "5 mins",
    "15min": "15 mins",
    "1hour": "1 hour",
    "1day": "1 day"
}

DURATION = {
    "1min": "30 D",
    "5min": "90 D",
    "15min": "180 D",
    "1hour": "1 Y",
    "1day": "5 Y"
}

# ====================================================

req_id = 0

for ticker in TICKERS:
    contract = security(ticker)

    for tf_name, tf_bar in TIMEFRAMES.items():
        histData(req_id, contract, DURATION[tf_name], tf_bar)
        save_to_csv(
            app.data_store[req_id],
            f"{ticker}_{tf_name}.csv"
        )
        req_id += 1
        time.sleep(10)

time.sleep(2)
app.disconnect()
