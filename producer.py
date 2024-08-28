import os
import time
import random
import json
from kafka import KafkaProducer
import pandas as pd
import datetime

def main():
    T = datetime.datetime.now()
    print("Current Time: ", T)

    # Read csv file: traffic data
    df = pd.read_csv('out.csv')
    l = df['t'].unique() 

    # Create topic on broker and produce messages
    KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC_TEST = os.environ.get("KAFKA_TOPIC_TEST", "vehicle_positions") #change topic's name to vehicles_positions according to the excercise
    KAFKA_API_VERSION = os.environ.get("KAFKA_API_VERSION", "7.3.1")
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        api_version=KAFKA_API_VERSION,
    )
    counter = 0
    for i in range(len(l)):
        df_new = df[(df["t"] == l[i]) & (df["link"] != 'waiting_at_origin_node')].copy()
        df_new['t'] = (T + datetime.timedelta(0,int(l[i]))).strftime('%Y-%m-%d %H:%M:%S')
        df_new = df_new.drop('dn', axis=1)
        message = df_new.to_dict(orient='records')
        for m in message:
            # print(m)
            counter = counter + 1
            # print(".", end='')
            producer.send(
                KAFKA_TOPIC_TEST,
                json.dumps(m).encode("utf-8"),
            )
            time.sleep(random.randint(1,3))
    producer.flush()
    print(counter)


if __name__ == "__main__":
    main()