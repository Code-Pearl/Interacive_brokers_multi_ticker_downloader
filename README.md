
A Python script for downloading historical market data from Interactive Brokers TWS/IB Gateway with custom date ranges and timeframes. The script formats data similarly to NQH6 files, including up/down volume and tick counts.

## Features

- **Multi-ticker support**: Download historical data for multiple symbols in a single run
    
- **Custom date ranges**: Specify start and end dates for data retrieval
    
- **Flexible timeframes**: Choose from various bar sizes (1 min, 5 mins, 1 hour, 1 day, etc.)
    
- **NQH6 format output**: Data is formatted with up/down volume and tick count columns
    
- **Easy configuration**: Simple parameter modification for different data requirements
    

## Prerequisites

### Required Software

- Python 3.7 or higher
    
- Interactive Brokers TWS or IB Gateway running
    
- ibapi Python package
    

### Installation

1. **Install the IB API Python package**:
    

bash

pip install ibapi

2. **Configure Interactive Brokers**:
    
    - Launch TWS or IB Gateway
        
    - Enable API connections (Settings → API → Settings)
        
    - Set socket port to 7497 for paper trading or 7496 for live trading
        
    - Ensure "Enable ActiveX and Socket Clients" is checked
        

## Script Configuration

### Key Parameters to Customize

Edit these variables in the script to customize your data download:

python

# Time and date parameters
START_DATE = ""  # Format: "YYYYMMDD HH:MM:SS", leave empty for automatic calculation
END_DATE = ""    # Format: "YYYYMMDD HH:MM:SS", leave empty for current time
DURATION = "11 D"  # Duration: '1 D', '1 W', '1 M', '1 Y', etc.
CANDLE_SIZE = "1 min"  # Timeframe: '1 min', '5 mins', '1 hour', '1 day'
WHAT_TO_SHOW = "TRADES"  # Options: TRADES, MIDPOINT, BID, ASK

# Ticker list
tickers = ["AMD"]  # Add more tickers as needed

### Contract Configuration

Modify the `security()` function for different security types:

python

# Default is stocks on NASDAQ
def security(symbol, sec_type="STK", currency="USD", exchange="ISLAND"):

For other security types:

- Futures: `sec_type="FUT"`, specify exchange (e.g., "CME")
    
- Forex: `sec_type="CASH"`, currency pair (e.g., "EUR.USD")
    
- Options: `sec_type="OPT"`
    

## Usage

### Basic Usage

1. **Start Interactive Brokers TWS/IB Gateway**
    
2. **Run the script**:
    

bash

python ib_hist_multi_ticker.py

### Custom Examples

**Example 1: Download 30 days of 5-minute data**

python

START_DATE = "20240101 09:30:00"
END_DATE = "20240130 16:00:00"
DURATION = "30 D"
CANDLE_SIZE = "5 mins"
tickers = ["AAPL", "MSFT", "GOOGL"]

**Example 2: Download current week's 1-hour data**

python

START_DATE = ""
END_DATE = ""
DURATION = "1 W"
CANDLE_SIZE = "1 hour"
tickers = ["SPY", "QQQ", "IWM"]

**Example 3: Download specific date range with 1-day bars**

python

START_DATE = "20240101"
END_DATE = "20241231"
DURATION = "1 Y"
CANDLE_SIZE = "1 day"
tickers = ["NVDA", "TSLA", "META"]

## Output Format

Data is saved to CSV files in the `historical_data` directory with the following NQH6-style format:

|Column|Description|Example|
|---|---|---|
|`<Date>`|Date of the bar|20241224|
|`<Time>`|Time of the bar|09:30:00|
|`<Open>`|Opening price|175.50|
|`<High>`|Highest price|176.25|
|`<Low>`|Lowest price|175.25|
|`<Close>`|Closing price|176.00|
|`<UpVolume>`|Volume on upticks (set to 0)|0|
|`<DownVolume>`|Volume on downticks (set to 0)|0|
|`<TotalVolume>`|Total volume|1234567|
|`<UpTicks>`|Number of upticks (set to 0)|0|
|`<DownTicks>`|Number of downticks (set to 0)|0|
|`<TotalTicks>`|Total ticks (set to 0)|0|
|`<OpenInterest>`|Open interest (set to 0)|0|

**Note**: Up/down volume and tick counts are currently set to 0 as this data requires specialized requests through IB API.

## File Structure

text

historical_data_downloader/
├── ib_hist_multi_ticker.py    # Main script
├── historical_data/           # Output directory (created automatically)
│   ├── AMD 1min.txt          # Example output file
│   └── ...                    # Other ticker files
└── README.md                  # This file

## Troubleshooting

### Common Issues

1. **Connection Error: Cannot connect to 127.0.0.1:7497**
    
    - Ensure TWS/IB Gateway is running
        
    - Verify API is enabled in TWS settings
        
    - Check the correct port (7497 for paper, 7496 for live)
        
2. **No Data Received**
    
    - Verify the ticker symbol is correct
        
    - Check market hours for the requested timeframe
        
    - Ensure you have data permissions for the security type
        
3. **Timeout Errors**
    
    - Increase the timeout in `data_received.wait(timeout=60)`
        
    - Check internet connection
        
    - Reduce number of concurrent requests
        

### Port Configuration

Default Interactive Brokers ports:

- **TWS Live Trading**: 7496
    
- **TWS Paper Trading**: 7497
    
- **IB Gateway Live**: 4001
    
- **IB Gateway Paper**: 4002
    

Modify the connection line in the script if needed:

python

app.connect("127.0.0.1", 7497, clientId=2)  # Change port as needed

## Limitations

1. **Rate Limits**: Interactive Brokers imposes rate limits on historical data requests
    
2. **Data Availability**: Historical data availability varies by security type and exchange
    
3. **Up/Down Data**: Up/down volume and tick counts require additional API calls not implemented in this version
    
4. **Maximum Data**: IB API has limits on how much historical data can be retrieved in one request
    

## Future Enhancements

Potential improvements for this script:

- Add support for up/down volume and tick data
    
- Implement pagination for large date ranges
    
- Add error recovery and retry logic
    
- Include more data fields (VWAP, trades count, etc.)
    
- Add progress indicators for multiple tickers
    
- Support for streaming real-time data
    

## Legal Disclaimer

This software is for educational purposes only. Use at your own risk. The authors are not responsible for any trading losses or damages resulting from the use of this software. Always test strategies with paper trading before using real money.

## License

This project is provided as-is without warranty. Users are responsible for complying with Interactive Brokers' API terms of service and any applicable regulations.