import sys
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pymongo import MongoClient

def save_raw_data(batch_df, batch_id):
    batch_df.write \
        .format("mongodb") \
        .mode("append") \
        .option("database", "traffic") \
        .option("collection", "raw_data") \
        .save()

# save proc
def save_processed_data(batch_df, batch_id):
    batch_df.write \
        .format("mongodb") \
        .mode("append") \
        .option("database", "traffic") \
        .option("collection", "processed_data") \
        .option("upsertDocument", True) \
        .option("idFieldList", "time, link") \
        .option("operationType", "update") \
        .save()
    
def init_db():
    client = MongoClient('localhost', 27017)

    # Drop the database if it exists & Create the new database
    if "traffic" in client.list_database_names():
        client.drop_database("traffic")
    client["traffic"]

if __name__ == "__main__":
    #clear database
    init_db()

    # Initializing Spark session
    spark = SparkSession\
        .builder\
        .appName("MySparkSession")\
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,"
                "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0") \
        .config("spark.mongodb.write.connection.uri", "mongodb://127.0.0.1/traffic.raw_data") \
        .getOrCreate()
        
    schema = StructType([
        StructField("name", StringType(), True),
        StructField("origin", StringType(), True),
        StructField("destination", StringType(), True),
        StructField("time", StringType(), True),
        StructField("link", StringType(), True),
        StructField("position", DoubleType(), True),
        StructField("spacing", DoubleType(), True),
        StructField("speed", DoubleType(), True)
    ])

    # Streaming data from Kafka topic as a dataframe
    lines = spark\
        .readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", 'localhost:9092')\
        .option('subscribe', 'vehicle_positions')\
        .load() 
    
    lines = lines\
        .selectExpr("CAST(value AS STRING)")\
        .select(from_json(col("value"), schema).alias("data")).select("data.*")
 
    # Writing dataframe (raw data) to database
    raw_data = lines \
        .writeStream \
        .foreachBatch(save_raw_data) \
        .start()
    
    # Processing dataframe 
    lines = lines\
        .filter(lines.link!='trip_end') \
        .select("time", "link", "speed")\
        .groupBy("time", "link")\
        .agg(avg("speed").alias("avg_SPEED"),
             count("link").alias("num_VEHICLES"))\
        .select("time", "link", "avg_SPEED", "num_VEHICLES")

    # Writing dataframe (processed data) to database in update mode
    processed_data = lines \
        .writeStream \
        .foreachBatch(save_processed_data) \
        .outputMode("update")\
        .start()
        
    # Terminates the stream on abort
    raw_data.awaitTermination()
    processed_data.awaitTermination()