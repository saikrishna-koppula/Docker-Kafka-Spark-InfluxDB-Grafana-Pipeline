from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import datetime
import pandas as pd
import json
from confluent_kafka import Producer

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load API credentials
API_KEY = os.getenv("APCA-API-KEY-ID")
API_SECRET = os.getenv("APCA-API-SECRET-KEY")

# Alpaca Client (No API keys needed for free historical data)
client = StockHistoricalDataClient(api_key=API_KEY, secret_key=API_SECRET)

# Load stock symbols from CSV file
symbols_data = pd.read_csv('asset_details.csv')
symbols_data = symbols_data[(symbols_data['class'] == "us_equity") & (symbols_data['status'] == "active")]
symbols_list = list(symbols_data.symbol)

# Override the list with top stocks of interest
symbols_list = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC',
    'BA', 'DIS', 'WMT', 'PG', 'JPM', 'V', 'MA', 'PYPL', 'XOM', 'CVX',
    'KO', 'PEP', 'T', 'IBM', 'GE', 'BABA', 'NKE', 'GS', 'MS', 'ADBE',
    'ORCL', 'TSM', 'CSCO', 'QCOM', 'PFE', 'MRNA', 'UNH', 'JNJ', 'COST', 'HD',
    'MCD', 'SBUX', 'LMT', 'RTX', 'CAT', 'FDX', 'UPS', 'GM', 'F', 'UBER'
]

# Creating request object
request_params = StockBarsRequest(
    symbol_or_symbols=symbols_list,
    timeframe=TimeFrame.Day,
    start=datetime.datetime(2006, 9, 1),
    end=datetime.datetime(2025, 9, 7),
    feed="iex"
)

# Retrieve daily bars
bars = client.get_stock_bars(request_params)

# Convert to DataFrame
bars_df = bars.df
bars_df['timestamp'] = bars_df.index.get_level_values(1)

# Kafka Configuration
conf = {'bootstrap.servers': 'kafka:9092'}
producer = Producer(conf)

# Callback function to check delivery status
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Kafka topic for stock data
topic = 'Stocks'

for symbol_item in symbols_list:
    data_to_send = {
        'data_agg_level': 'Day',
        'symbol_group': 'Stocks',
        'symbol': symbol_item,
        'data': bars_df.loc[symbol_item].to_json(orient='records')
    }
    producer.produce(topic, key=symbol_item, value=json.dumps(data_to_send), callback=delivery_report)
    producer.flush()