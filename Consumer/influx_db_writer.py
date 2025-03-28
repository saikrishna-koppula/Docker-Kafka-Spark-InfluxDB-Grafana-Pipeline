from pyspark.sql import SparkSession
from influxdb_client import InfluxDBClient, Point, WriteOptions
import pandas
from datetime import datetime
from pyspark.sql.functions import col, min, max

# InfluxDB Connection Details
INFLUXDB_URL = "http://influxdb:8086"  # Replace with your InfluxDB URL
INFLUXDB_TOKEN = "8720fe75-3d11-408c-8984-c31ea9457c4c"  # Use your InfluxDB token
INFLUXDB_ORG = "primary"  # Organization name in InfluxDB
DEFAULT_INFLUXDB_BUCKET = "Data_Bucket"  # Bucket where data will be written

# Initialize InfluxDB Client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10000))

def write_to_influxdb(df, epoch_id, INFLUXDB_BUCKET = DEFAULT_INFLUXDB_BUCKET):
    
    print("---------Exactly Before Writing to  INFLUX DB!!---------")

    df.filter(col("data_agg_level") == "Min").groupBy("data_agg_level", "symbol_group", "symbol").agg(
        min("timestamp").alias("min_time"),
        max("timestamp").alias("max_time")
    ).show(truncate=False)

    # Convert the Spark DataFrame to Pandas for easier manipulation
    pandas_df = df.toPandas()

    # Convert DataFrame to a list of Points for InfluxDB
    points = [
        # Point("data")
        Point(row["data_agg_level"])
            .tag("symbol_group", row["symbol_group"])
            .tag("symbol", row["symbol"])
            .field("open", float(row["open"]))
            .field("high", float(row["high"]))
            .field("low", float(row["low"]))
            .field("close", float(row["close"]))
            .field("trade_count", int(row["trade_count"]))
            .field("volume", float(row["volume"]))
            .field("vwap", float(row["vwap"]))
            #.field("event_time", row["timestamp"])
            .time(row["timestamp"])
            #.field("event_time", datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S").isoformat() + "Z")
            #.time(datetime.now())
        for _, row in pandas_df.iterrows()
    ]
    
    # Batch write to InfluxDB using the write API
    if points:
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points, write_precision="s")
        print(f"Batch {epoch_id} written successfully! to: {INFLUXDB_BUCKET}")