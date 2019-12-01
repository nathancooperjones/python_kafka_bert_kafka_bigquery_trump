import json

from kafka import KafkaConsumer


consumer = KafkaConsumer('kafka_1_to_kafka_2',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

for msg in consumer:
    sentence_to_encode = msg.value['sentence_to_encode']
    sentence_embedding = msg.value['sentence_embedding']
    print(sentence_to_encode, sentence_embedding)
