import json

from kafka import KafkaConsumer, KafkaProducer
from sentence_transformers import SentenceTransformer


consumer = KafkaConsumer(topics='sentence_to_kafka_1',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
model = SentenceTransformer('bert-base-nli-mean-tokens')

for msg in consumer:
    print(msg)
    print(msg.value)
    # access the message somehow
    # sentence_to_encode = msg.value
    # encoded_sentence = model.encode([sentence_to_encode])
    # sentence_json = {'sentence_to_encode': encoded_sentence[0],
    #                  'sentence_embedding': encoded_sentence[1]}
    # producer.send('kafka_1_to_kafka_2', sentence_json)
