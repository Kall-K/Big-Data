# Big-Data
commands:
- kafka_2.13-3.7.1/bin/zookeeper-server-start.sh kafka_2.13-3.7.1/config/zookeeper.properties

- kafka_2.13-3.7.1/bin/kafka-server-start.sh  kafka_2.13-3.7.1/config/server.properties

- big_data$ python3 producer.py

- python3 big_data/spark_processor.py

- ./kafka-topics.sh --delete --topic traffic --bootstrap-server localhost:9092
- ./kafka-topics.sh --list --bootstrap-server localhost:9092

- mongod --dbpath /var/lib/mongo --logpath /var/log/mongodb/mongod.log --fork
- $ mongosh
