import json
from kafka import KafkaConsumer

def receiver_stats(value):
    rec_list = list()
    receivers = value["receiving"]
    for value in receivers.values():
        rec_list.append(value)
    return rec_list

if __name__ == "__main__":
    topic_name = "raw_stats"
    
    receivers = list()
    consumer = KafkaConsumer(topic_name, auto_offset_reset='earliest', bootstrap_servers=['localhost:9092'], 
                             enable_auto_commit=False, consumer_timeout_ms=1000, value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for message in consumer:
        print ("topic:%s part: %d offset: %d, key=%s" % (message.topic, message.partition, message.offset))
        recs = receiver_stats(message.value)
        receivers += recs

    print(receivers)
    if consumer:
        consumer.close()