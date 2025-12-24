"""
IBAPI - Getting historical data (multiple tickers) with custom date range and timeframe

This script downloads data the same way as ib_hist_multi_ticker.py but formats it
like the NQH6 files with up/down volume and tick counts, and allows custom date ranges
and timeframes.
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import os
import csv
from datetime import datetime, timedelta

class TradingApp(EWrapper, EClient):
    """
    Handles the interface for trading applications by integrating `EWrapper` and `EClient`.

    This class is used to manage interactions with a trading platform, specifically
    for retrieving and storing historical data, handling asynchronous event-driven
    processes, and managing errors during requests. It ensures data consistency and
    provides mechanisms for signaling when data retrieval is complete.

    :ivar data_received: An event used to signal the completion of data retrieval.
    :type data_received: threading.Event
    :ivar data_store: A dictionary for storing retrieved historical data, organized
        by request id (reqId).
    :type data_store: dict[int, list]

    """
    def __init__(self):
        EClient.__init__(self,self)
        self.data_received = threading.Event()  # Initialize the threading event
        self.data_store = {}  # Dictionary to store retrieved data
        
    def historicalData(self, reqId, bar):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)

        # Append bar data to the appropriate ticker's storage
        if reqId not in self.data_store:
            self.data_store[reqId] = []

        # Parse the date string to separate date and time
        date_str = bar.date
        if ' ' in date_str:  # If date includes time
            date_part, time_part = date_str.split(' ', 1)
        else:
            date_part = date_str
            time_part = "00:00:00"
        
        # Format data to match NQH6 format: Date, Time, Open, High, Low, Close, UpVolume, DownVolume, TotalVolume, UpTicks, DownTicks, TotalTicks, OpenInterest
        # For basic historical data, we'll set volume/tick counts to 0 since they're not available in this format
        # OpenInterest is also set to 0 for now
        formatted_row = [date_part, time_part, bar.open, bar.high, bar.low, bar.close, 0, 0, bar.volume, 0, 0, 0, 0]
        self.data_store[reqId].append(formatted_row)

    def historicalDataEnd(self, reqId, start, end):
        print(f"HistoricalDataEnd. ReqId: {reqId}, Start: {start}, End: {end}")
        self.data_received.set()  # Signal that data is complete

    def error(self, reqId, errorCode, errorString):
        print(f"Error. ReqId: {reqId}, Code: {errorCode}, Msg: {errorString}")
        
def websocket_con():
    app.run()
    
app = TradingApp()

# Default ports:
# TWS live session: 7496
# TWS paper session: 7497
# IB Gateway live session: 4001
# IB Gateway paper session: 4002
app.connect("127.0.0.1", 7497, clientId=2)

# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1) # some latency added to ensure that the connection is established

# creating object of the Contract class - will be used as a parameter for other function calls
# edit the sec_type, currency and exchange variables as needed.
def security(symbol,sec_type="STK",currency="USD",exchange="ISLAND"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract 

def histData(req_num, contract, duration, candle_size, end_date_time='', whatToShow='TRADES'):
    app.data_received.clear()

    app.reqHistoricalData(
        reqId=req_num,
        contract=contract,
        endDateTime=end_date_time,  # Can be empty string for current time, or specific date/time
        durationStr=duration,
        barSizeSetting=candle_size,
        whatToShow=whatToShow,  # TRADES, MIDPOINT, BID, ASK, etc.
        useRTH=1,
        formatDate=1,
        keepUpToDate=0,
        chartOptions=[]
    )

    if not app.data_received.wait(timeout=60):
        print(f"Timeout for request {req_num}")

# Save data to CSV in NQH6 format
def save_to_csv(data, filename):
    header = ["<Date>", "<Time>", "<Open>", "<High>", "<Low>", "<Close>", "<UpVolume>", "<DownVolume>", "<TotalVolume>", "<UpTicks>", "<DownTicks>", "<TotalTicks>", "<OpenInterest>"]
    os.makedirs("historical_data", exist_ok=True)
    filepath = os.path.join("historical_data", filename)
    
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # Write the header
        writer.writerows(data)   # Write the data

# Define parameters for date range and timeframe
# Example: start_date = "20240920 09:30:00", end_date = "20241224 16:00:00"
# Duration examples: '1 D', '1 W', '1 M', '1 Y', etc.
# Candle size examples: '1 min', '5 mins', '1 hour', '1 day', etc.

# You can customize these parameters:
START_DATE = ""  # Format: YYYYMMDD HH:MM:SS, or leave empty for current time
END_DATE = ""    # Format: YYYYMMDD HH:MM:SS, or leave empty for current time
DURATION = "11 D"  # How far back to go if no START_DATE specified
CANDLE_SIZE = "1 min"  # Timeframe: '1 min', '5 mins', '1 hour', '1 day', etc.
WHAT_TO_SHOW = "TRADES"  # TRADES, MIDPOINT, BID, ASK

# Edit/add/remove tickers as needed.
tickers = ["AMD"]

req_id = 0
for ticker in tickers:
    contract = security(ticker)
    
    # Determine end date/time - use provided END_DATE or empty string for current time
    end_date_time = END_DATE if END_DATE else ""
    
    # Determine start date based on duration if START_DATE is not provided
    if START_DATE:
        start_date_time = START_DATE
    else:
        # Calculate start date based on duration
        # For this implementation, we'll use the durationStr parameter instead
        start_date_time = ""
    
    print(f"Fetching historical data for {ticker} from {start_date_time or 'latest available'} to {end_date_time or 'current time'}...")
    
    # Request historical data
    histData(req_id, contract, DURATION, CANDLE_SIZE, end_date_time, WHAT_TO_SHOW)
    
    # Save the data if available
    if req_id in app.data_store and app.data_store[req_id]:
        save_to_csv(
            app.data_store[req_id],
            f"{ticker} {CANDLE_SIZE.replace(' ', '')}.txt"
        )
        print(f"Saved data for {ticker}")
    else:
        print(f"No data received for {ticker}")
    
    req_id += 1
    time.sleep(15)  # some latency added to ensure that the contract details request has been processed

# Disconnect after all requests are done
time.sleep(2)
app.disconnect()
