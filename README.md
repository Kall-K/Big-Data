# Big Data Traffic Streaming Pipeline

This project simulates traffic data with UXsim, streams it through Kafka, processes it with Spark, and stores the results in MongoDB.

## Files

- `producer.py`: runs the traffic simulation and sends vehicle events to Kafka
- `spark_processor.py`: reads Kafka events, stores raw data in MongoDB, and writes aggregated results
- `consumer.py`: optional Kafka consumer for debugging
- `queries.py`: runs example MongoDB queries on the stored data

## Requirements

You need these installed locally:

- Python 3
- Java 8+ (required for Apache Spark / PySpark)
- Apache Kafka `3.7.1`
- ZooKeeper
- MongoDB
- Apache Spark

Python packages:

```bash
pip install kafka-python uxsim pyspark pymongo pandas
```

## Run Order

### 1. Start ZooKeeper

```bash
kafka_2.13-3.7.1/bin/zookeeper-server-start.sh kafka_2.13-3.7.1/config/zookeeper.properties
```

### 2. Start Kafka broker

```bash
kafka_2.13-3.7.1/bin/kafka-server-start.sh kafka_2.13-3.7.1/config/server.properties
```

### 3. Start MongoDB

```bash
mongod --dbpath /var/lib/mongo --logpath /var/log/mongodb/mongod.log --fork
```

### 4. Start the Spark processor

```bash
python3 spark_processor.py
```

### 5. Run the producer

```bash
python3 producer.py
```

### 6. Optional: inspect Kafka messages

```bash
python3 consumer.py
```

### 7. Run queries

```bash
python3 queries.py
```

### 8. Open MongoDB shell

```bash
mongosh
```

## Useful Kafka Commands

Show topics:

```bash
./kafka-topics.sh --list --bootstrap-server localhost:9092
```

Delete topic:

```bash
./kafka-topics.sh --delete --topic traffic --bootstrap-server localhost:9092
```

## Notes

- Kafka is expected on `localhost:9092`
- MongoDB is expected on `localhost:27017`
- Java must be installed and available on your `PATH` when running `spark_processor.py`
- `spark_processor.py` clears the `traffic` database when it starts
