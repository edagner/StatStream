import os
import json
from kafka import KafkaProducer


def retrieve_stats():
    filename = "Superbowl_53.json"
    with open(filename, "rb") as json_file:
        data = json.load(json_file)
        stats_dict = dict()
        home_stats = data["2019020300"]["home"]["stats"]
        away_stats = data["2019020300"]["away"]["stats"]
        stats_dict["away"] = away_stats
        stats_dict["home"] = home_stats
    return stats_dict


def create_producer():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    return producer


def send_message(producer_instance, topic_name, key_msg, value_msg):
    try:
        key_bytes = bytes(str(key_msg), encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_msg)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as e:
        print('Message failed to publish.')
        print(e)


if __name__ == "__main__":
    topic_name = "raw_stats"
    game_stats = retrieve_stats()
    prod = create_producer()
    for team, stats in game_stats.items():
        #print(team, stats)
        send_message(prod, topic_name, team, stats)
    if prod:
        prod.close()