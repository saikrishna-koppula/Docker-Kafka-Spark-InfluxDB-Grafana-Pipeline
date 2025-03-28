from pyspark.sql import SparkSession
import time
import json
from pyspark.sql.functions import lit, col, from_unixtime, from_json, explode, from_utc_timestamp, min, max
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, ArrayType, LongType
from influx_db_writer import write_to_influxdb

KAFKA_BROKER = "kafka:9092"
subscribe_topic  = 'Crypto_Currency, Stocks'

spark = SparkSession.builder \
    .appName("Spark Consumer for Crypto Topic") \
    .master("local[*]") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/spark_checkpoint") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

data_schema = ArrayType(
    StructType([
        StructField('close', DoubleType(), True),
        StructField('high', DoubleType(), True),
        StructField('low', DoubleType(), True),
        StructField('open', DoubleType(), True),
        StructField('timestamp', LongType(), True),
        StructField('trade_count', DoubleType(), True),
        StructField('volume', DoubleType(), True),
        StructField('vwap', DoubleType(), True)
    ]), True)

schema = StructType([
    StructField("data_agg_level", StringType(), True),
    StructField("symbol_group", StringType(), True),
    StructField("symbol", StringType(), True),
    StructField("data", StringType(), True)
])

def process_batch(df, epoch_id):
    print(f"Processing batch {epoch_id} with {df.count()} messages")

    parsed_df = df.withColumn("message_json", from_json(col("message"), schema)) \
                  .select(col("message_json.data_agg_level"), col("message_json.symbol_group"), col("message_json.symbol"), col("message_json.data"))
    #parsed_df.show(truncate=True)


    #data_df = parsed_df.select(col("data"))
    #inferred_schema = spark.read.json(data_df.rdd.map(lambda row: row["data"])).schema
    # The above 2 lines of code was used to dynamically infer schema and then I manually hardcoded the schema as it not always necessary to do all this 
    parsed_df = parsed_df.withColumn("data", from_json(col("data"), data_schema))
    parsed_df = parsed_df.withColumn("data", explode("data"))
    
    parsed_df = parsed_df.select(
        col('data_agg_level'),
        col("symbol_group"),
        col("symbol"),
        from_unixtime(col("data.timestamp") / 1000).alias("timestamp"),
        col("data.open").alias("open"),
        col("data.high").alias("high"),
        col("data.low").alias("low"),
        col("data.close").alias("close"),
        col("data.trade_count").alias("trade_count"),
        col("data.volume").alias("volume"),
        col("data.vwap").alias("vwap")
    )

    #parsed_df = parsed_df.withColumn("timestamp", from_utc_timestamp(col("timestamp"), "America/New_York"))

    #parsed_df.filter(col("data_agg_level") == "Day").select("data_agg_level", "symbol_group", "symbol").distinct().show(truncate=False)
    #parsed_df.filter(col("data_agg_level") == "Min").select("data_agg_level", "symbol_group", "symbol").distinct().show(truncate=False)
    
    # parsed_df.filter(col("data_agg_level") == "Day").groupBy("data_agg_level", "symbol_group", "symbol").agg(
    #     min("timestamp").alias("min_time"),
    #     max("timestamp").alias("max_time")
    # ).show(truncate=False)
    parsed_df.filter(col("data_agg_level") == "Min").groupBy("data_agg_level", "symbol_group", "symbol").agg(
        min("timestamp").alias("min_time"),
        max("timestamp").alias("max_time")
    ).show(truncate=False)
    

    #write_to_influxdb(parsed_df.filter(col("data_agg_level") == "Day"), epoch_id, "Day_Bucket")
    #write_to_influxdb(parsed_df.filter(col("data_agg_level") == "Min"), epoch_id, "Minute_Bucket")
    
    write_to_influxdb(parsed_df, epoch_id)

    print("Exiting the function------", epoch_id)


df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", subscribe_topic) \
    .option("group.id","crypto_topic_spark") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert Kafka message value from binary to string
messages = df.selectExpr("CAST(value AS STRING) as message")

query = messages.writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .start()

query.awaitTermination()