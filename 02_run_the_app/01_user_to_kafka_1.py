import json

from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    sentence = input("Type a sentence (or 'q' to quit): ")
    if sentence.strip() == 'q':
        break
    sentence_json = {'sentence_to_encode': sentence}
    future = producer.send('sentence_to_kafka_1', sentence_json)
    result = future.get(timeout=60)

print('I hope you learned how Trump you are!')
