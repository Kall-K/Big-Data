# Big-Data
### commands:
#### start zookeeper 
- kafka_2.13-3.7.1/bin/zookeeper-server-start.sh kafka_2.13-3.7.1/config/zookeeper.properties
#### start kafka broker
- kafka_2.13-3.7.1/bin/kafka-server-start.sh  kafka_2.13-3.7.1/config/server.properties
#### run producer
- python3 big_data/producer.py
#### run spark consumer, processor
- python3 big_data/spark_processor.py
#### delete topic
- ./kafka-topics.sh --delete --topic traffic --bootstrap-server localhost:9092
#### show topics
- ./kafka-topics.sh --list --bootstrap-server localhost:9092
#### run mongodb
- mongod --dbpath /var/lib/mongo --logpath /var/log/mongodb/mongod.log --fork
#### run mongodb shell
- $ mongosh
