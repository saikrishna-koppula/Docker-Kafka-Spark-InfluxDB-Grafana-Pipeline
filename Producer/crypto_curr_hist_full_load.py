from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
import datetime
import time
from confluent_kafka import Producer
import json
from confluent_kafka.admin import AdminClient, NewTopic
import pandas as pd

# No keys required for crypto data
client = CryptoHistoricalDataClient()

symbols_data = pd.read_csv('asset_details.csv')
symbols_data = symbols_data[(symbols_data['class']=="crypto") & (symbols_data['status']=="active")]
symbols_list = list(symbols_data.symbol)

# Override the symbols list as we do not want to load data for all active symbols, but only for the Crypto Curencies that we want.
symbols_list = [
    'MKR/USD', 'AVAX/USD', 'AAVE/USD', 'DOT/USD', 'GRT/USD', 
    'SUSHI/USD', 'UNI/USD', 'USDC/USD', 'USDT/USD', 'YFI/USD', 
    'BAT/USD', 'BCH/USD', 'CRV/USD', 'DOGE/USD', 'ETH/USD', 
    'LINK/USD', 'LTC/USD', 'SOL/USD', 'XRP/USD', 'XTZ/USD', 
    'TRUMP/USD', 'SHIB/USD', 'PEPE/USD', 'BTC/USD']

# Creating request object
request_params = CryptoBarsRequest(
  #symbol_or_symbols=["BTC/USD"],
  symbol_or_symbols=symbols_list,
  timeframe=TimeFrame.Day,
  start=datetime.datetime(2006, 9, 1),
  end=datetime.datetime(2025, 9, 7)
)

# Retrieve daily bars for Bitcoin in a DataFrame and printing it
bars = client.get_crypto_bars(request_params)

# Convert to dataframe
bars_df = bars.df
bars_df['timestamp'] = bars_df.index.get_level_values(1)

# Kafka Configuration
conf = {'bootstrap.servers': 'kafka:9092'}  # Change if Kafka is remote
producer = Producer(conf)

# Callback function to check delivery status
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

#create a new Kafka topic
topic = 'Crypto_Currency'

# You njo longer have ti cerate topic from the program because it is being taken care as part of YAML file.
# admin_client = AdminClient(conf)
# topic_list = [NewTopic(topic, num_partitions=3, replication_factor=1)]
# admin_client.create_topics(topic_list)


for symbol_item in symbols_list:
    #data_to_send = bars_df.loc[symbol_item].to_json(orient = 'records')
    data_to_send = {
        'data_agg_level':'Day',
        'symbol_group': 'Crypto',
        'symbol': symbol_item,
        'data': bars_df.loc[symbol_item].to_json(orient = 'records')
    }
    #print(data_to_send)
    producer.produce(topic, key = symbol_item, value = json.dumps(data_to_send), callback = delivery_report)
    producer.flush()
    #print(data_to_send)