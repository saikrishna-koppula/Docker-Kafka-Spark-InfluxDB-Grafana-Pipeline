from alpaca.data.live import StockDataStream
from alpaca.trading.client import TradingClient
import os
from dotenv import load_dotenv
import asyncio
from dataclasses import asdict
import json
from confluent_kafka import Producer
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Load API credentials
API_KEY = os.getenv("APCA-API-KEY-ID")
API_SECRET = os.getenv("APCA-API-SECRET-KEY")

print(API_KEY)
print(API_SECRET)

# Load stock symbols from CSV file
symbols_data = pd.read_csv('asset_details.csv')
symbols_data = symbols_data[(symbols_data['class'] == "us_equity") & (symbols_data['status'] == "active")]
symbols_list = list(symbols_data.symbol)

# Override the symbols list with top stocks of interest
symbols_list = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC',
    'BA', 'DIS', 'WMT', 'PG', 'JPM', 'V', 'MA', 'PYPL', 'XOM', 'CVX',
    'KO', 'PEP', 'T', 'IBM', 'GE', 'BABA', 'NKE', 'GS', 'MS', 'ADBE',
    'ORCL', 'TSM', 'CSCO', 'QCOM', 'PFE', 'MRNA', 'UNH', 'JNJ', 'COST', 'HD',
    'MCD', 'SBUX', 'LMT', 'RTX', 'CAT', 'FDX', 'UPS', 'GM', 'F', 'UBER'
]

trading_client = TradingClient(API_KEY, API_SECRET)

# Get market clock status
clock = trading_client.get_clock()
print(f"Market Open: {clock.is_open}")
print(f"Next Open: {clock.next_open}")
print(f"Next Close: {clock.next_close}")

# Callback function to check delivery status
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Kafka Configuration
conf = {'bootstrap.servers': 'kafka:9092'}  # Change if Kafka is remote
producer = Producer(conf)
#create a new Kafka topic
topic = 'Crypto_Currency'


# Define a callback function to handle bar updates
async def on_bar(bar):
    bar_data = json.dumps([
        {
        "timestamp": int(bar.timestamp.timestamp() * 1000),
        "open": bar.open,
        "high": bar.high,
        "low": bar.low,
        "close": bar.close,
        "volume": bar.volume,
        "trade_count": bar.trade_count,
        "vwap": bar.vwap
    }])

    data_to_send = json.dumps({
        'data_agg_level': 'Min',
        'symbol_group': 'Stocks',
        "symbol": bar.symbol,
        "data": bar_data
    })

    producer.produce(topic, key="Stocks", value=data_to_send, callback=delivery_report)
    print(f"********Data Sent for {bar.symbol} for {bar.timestamp}*************")
    #print(data_to_send)

# Initialize the stock data stream client
stock_stream = StockDataStream(api_key=API_KEY, secret_key=API_SECRET)

stock_stream.subscribe_bars(on_bar, *symbols_list)

stock_stream.run()