import json

from kafka import KafkaConsumer


consumer = KafkaConsumer(topics='sentence_to_kafka_1',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

for msg in consumer:
    print(msg)
    print(msg.value)
