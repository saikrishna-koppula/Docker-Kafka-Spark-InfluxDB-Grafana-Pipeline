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

# You njo longer have to cerate topic from the program because it is being taken care as part of YAML file.
# admin_client = AdminClient(conf)
# topic_list = [NewTopic(topic, num_partitions=3, replication_factor=1)]
# admin_client.create_topics(topic_list)


absolute_end_date = datetime.datetime.now()
absolute_start_date = absolute_end_date - datetime.timedelta(days=7)

loop_hours = 1

# Loop from absolute_start_date to absolute_end_date, iterating by hour
current_time = absolute_start_date
while current_time < absolute_end_date:
    # Create request_params with dynamic start and end for every hour
    start_time = current_time
    end_time = current_time + datetime.timedelta(hours=loop_hours)
    request_params = CryptoBarsRequest(
        symbol_or_symbols=symbols_list,
        timeframe=TimeFrame.Minute,
        start=current_time,
        end=current_time + datetime.timedelta(hours=loop_hours)
    )

    # Retrieve the bars for the given time range
    bars = client.get_crypto_bars(request_params)

    # Convert to dataframe
    bars_df = bars.df
    bars_df['timestamp'] = bars_df.index.get_level_values(1)
    bars_df = bars_df.droplevel(1)

    for symbol_item in bars_df.index.unique():
        data_to_send = {
            'data_agg_level': 'Min',
            'symbol_group': 'Crypto',
            'symbol': symbol_item,
            'data': bars_df.loc[symbol_item].to_json(orient='records')
        }

        # Send data to Kafka
        producer.produce(topic, key=symbol_item, value=json.dumps(data_to_send), callback=delivery_report)
    print(f"***********************************Data Sent for {start_time} to {end_time}***************************")

    # Increment current_time by one hour
    current_time += datetime.timedelta(hours=loop_hours)

# Wait for any outstanding messages to be delivered and delivery reports to be received
producer.flush()


# -------------------------
#Below is the template code for aboeve Hour Loop concept

# import datetime

# # Set the end date to the current date and time
# end_date = datetime.datetime.now()

# # Set the start date to 7 days before the end date
# start_date = end_date - datetime.timedelta(days=7)

# # Loop from end_date to start_date, iterating by hour
# current_time = end_date
# while current_time >= start_date:
#     print(f"Current time: {current_time}")
#     current_time -= datetime.timedelta(hours=1)
