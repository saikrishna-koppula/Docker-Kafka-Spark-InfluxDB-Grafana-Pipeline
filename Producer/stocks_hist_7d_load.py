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

# Alpaca Client
client = StockHistoricalDataClient(api_key=API_KEY, secret_key=API_SECRET)

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

# Kafka Configuration
conf = {'bootstrap.servers': 'kafka:9092'}
producer = Producer(conf)

# Callback function to check delivery status
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Kafka topic
topic = 'Stocks'

absolute_end_date = datetime.datetime.now()
absolute_start_date = absolute_end_date - datetime.timedelta(days=7)

loop_hours = 1

# Loop from absolute_start_date to absolute_end_date, iterating by hour
current_time = absolute_start_date
while current_time < absolute_end_date:
    start_time = current_time
    end_time = current_time + datetime.timedelta(hours=loop_hours)
    
    # Create request_params with dynamic start and end for every hour
    request_params = StockBarsRequest(
        symbol_or_symbols=symbols_list,
        timeframe=TimeFrame.Minute,
        start=start_time,
        end=end_time,
        feed="iex"
    )

    # Retrieve stock bars
    bars = client.get_stock_bars(request_params)
    bars_df = bars.df

    if bars_df.empty:
        print(f"No data available for {start_time} to {end_time}. Skipping...")
    else:
        bars_df['timestamp'] = bars_df.index.get_level_values(1)
        bars_df = bars_df.droplevel(1)

        for symbol_item in bars_df.index.unique():
            data_to_send = {
                'data_agg_level': 'Min',
                'symbol_group': 'Stocks',
                'symbol': symbol_item,
                'data': bars_df.loc[symbol_item].to_json(orient='records')
            }
            
            # Send data to Kafka
            producer.produce(topic, key=symbol_item, value=json.dumps(data_to_send), callback=delivery_report)
        
        print(f"***********************************Data Sent for {start_time} to {end_time}***************************")
        
        # Increment current_time by one hour
    current_time += datetime.timedelta(hours=loop_hours)

# Wait for outstanding messages to be delivered
producer.flush()
