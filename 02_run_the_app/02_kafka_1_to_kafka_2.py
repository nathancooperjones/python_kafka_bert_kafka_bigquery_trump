import json

from kafka import KafkaConsumer, KafkaProducer
from sentence_transformers import SentenceTransformer


consumer = KafkaConsumer('sentence_to_kafka_1',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
model = SentenceTransformer('bert-base-nli-mean-tokens')

for msg in consumer:
    sentence_to_encode = msg.value['sentence_to_encode']
    encoded_sentence = model.encode([sentence_to_encode])[0].tolist()
    sentence_json = {'sentence_to_encode': sentence_to_encode,
                     'sentence_embedding': encoded_sentence}
    print(sentence_json)
    producer.send('kafka_1_to_kafka_2', sentence_json)
