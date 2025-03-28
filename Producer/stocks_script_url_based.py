import requests
import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values
from confluent_kafka import Producer
import json

# Load environment variables from .env file
load_dotenv()

# Load API credentials from environment variables
API_KEY = os.getenv("APCA-API-KEY-ID")
API_SECRET = os.getenv("APCA-API-SECRET-KEY")

asset_df = pd.read_csv('asset_details.csv')
asset_symbols_df = asset_df[(asset_df['class']=="us_equity") & (asset_df['status'] == "active")]['symbol'].dropna()[:50]
#asset_symbols = ",".join(asset_symbols_df)

asset_symbols = "AAPL"

# API request URL
#url = f"https://data.alpaca.markets/v2/stocks/bars?limit=1000&adjustment=raw&feed=sip&sort=asc&symbols={asset_symbols}&timeframe=1Min"

#url = f"https://data.alpaca.markets/v2/stocks/bars?symbols={asset_symbols}&timeframe=1Min&start=2024-01-03T00%3A00%3A00Z&end=2024-01-04T00%3A00%3A00Z&limit=1000&adjustment=raw&feed=sip&sort=asc"
url = "https://data.alpaca.markets/v2/stocks/bars?symbols=AAPL&timeframe=1Min&start=2025-03-03&end=2025-03-04&limit=1000&adjustment=raw&feed=sip&sort=asc"

print(url)

# Headers with API credentials
headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": API_SECRET
}

response = requests.get(url, headers=headers)

#print(response.text)


# Kafka Configuration
conf = {'bootstrap.servers': 'kafka:9092'}  # Change if Kafka is remote
producer = Producer(conf)

topic = 'Stocks'

# Load JSON data
parsed_data = json.loads(response.text)

# Initialize an empty list to store records
all_data = []

# Iterate through each symbol and its data
for symbol, bars in parsed_data["bars"].items():
    for bar in bars:
        bar["symbol"] = symbol  # Add symbol column
        all_data.append(bar)  # Append to list

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(all_data)

print(df.head())

# Convert timestamp to datetime
df["t"] = pd.to_datetime(df["t"])

# Rename the columns
df.rename(columns={
    'c': 'close',
    'h': 'high',
    'l': 'low',
    'n': 'trade_count',
    'o': 'open',
    't': 'timestamp',
    'v': 'volume',
    'vw': 'vwap',
    'symbol': 'symbol'
}, inplace=True)
df.set_index('symbol', inplace=True)

# Display the DataFrame with renamed columns
print(df.head())

# Display DataFrame
# print(df.head(50))
print(df.columns)

# Get distinct values from the 'symbol' column as a list
symbols_list = df.index.unique().tolist()

# Callback function to check delivery status
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

for symbol_item in symbols_list:
    #data_to_send = bars_df.loc[symbol_item].to_json(orient = 'records')
    data_to_send = {
        'data_agg_level':'Min',
        'symbol_group': 'Stocks',
        'symbol': symbol_item,
        'data': df.loc[symbol_item].to_json(orient = 'records')
    }
    #print(data_to_send)
    producer.produce(topic, key = symbol_item, value = json.dumps(data_to_send), callback = delivery_report)
    producer.flush()
    #print(data_to_send)
