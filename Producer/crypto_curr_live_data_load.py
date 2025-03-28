from alpaca.data.live import CryptoDataStream
from confluent_kafka import Producer
import json
from alpaca.trading.client import TradingClient

import os
from dotenv import load_dotenv

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
symbols_data = symbols_data[(symbols_data['class'] == "crypto") & (symbols_data['status'] == "active")]
symbols_list = list(symbols_data.symbol)

# Override the symbols list with top cryptocurrencies of interest
symbols_list = [
    'MKR/USD', 'AVAX/USD', 'AAVE/USD', 'DOT/USD', 'GRT/USD', 
    'SUSHI/USD', 'UNI/USD', 'USDC/USD', 'USDT/USD', 'YFI/USD', 
    'BAT/USD', 'BCH/USD', 'CRV/USD', 'DOGE/USD', 'ETH/USD', 
    'LINK/USD', 'LTC/USD', 'SOL/USD', 'XRP/USD', 'XTZ/USD', 
    'TRUMP/USD', 'SHIB/USD', 'PEPE/USD', 'BTC/USD']


trading_client = TradingClient(API_KEY, API_SECRET)

# Get market clock status
clock = trading_client.get_clock()
print(f"Market Open: {clock.is_open}")
print(f"Next Open: {clock.next_open}")
print(f"Next Close: {clock.next_close}")

# Kafka Configuration
conf = {'bootstrap.servers': 'kafka:9092'}  # Change if Kafka is remote
producer = Producer(conf)
#create a new Kafka topic
crypto_topic = 'Crypto_Currency'

# Callback function to check delivery status
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Define a callback function to handle crypto bar updates
async def on_crypto_bar(bar):
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
        'symbol_group': 'Crypto',
        "symbol": bar.symbol,
        "data": bar_data
    })

    producer.produce(crypto_topic, key="Crypto", value=data_to_send, callback=delivery_report)
    print(f"********Data Sent for {bar.symbol} for {bar.timestamp}*************")

# Initialize the crypto data stream client
crypto_stream = CryptoDataStream(api_key=API_KEY, secret_key=API_SECRET)

crypto_stream.subscribe_bars(on_crypto_bar, *symbols_list)

crypto_stream.run()
