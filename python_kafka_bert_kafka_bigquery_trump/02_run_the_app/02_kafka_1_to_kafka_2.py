import json
import threading

from google.cloud import bigquery
import joblib
from kafka import KafkaConsumer, KafkaProducer
from python_kafka_bert_kafka_bigquery_trump.config import (BERT_MODEL,
                                                           DATASET_ID,
                                                           PCA_FILENAME,
                                                           SHORT_RESULTS_TABLE_ID)
from sentence_transformers import SentenceTransformer


consumer = KafkaConsumer('sentence_to_kafka_1',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
model = SentenceTransformer(BERT_MODEL)
pca = joblib.load(PCA_FILENAME)

client = bigquery.Client()
table_ref = client.dataset(DATASET_ID).table(SHORT_RESULTS_TABLE_ID)
table = client.get_table(table_ref)


# a decorator to make a function run asynchronously
def run_function_async(func):
    def wrapped(arg):
        threading.Thread(target=func, args=(arg,)).start()
    return wrapped


@run_function_async
def encode_and_send(msg):
    sentence_to_encode = msg.value['sentence_to_encode']
    sentence_embedding = model.encode([sentence_to_encode])[0].tolist()

    sentence_embedding_pca = pca.transform([sentence_embedding])[0]

    row_to_insert = [(sentence_to_encode, sentence_embedding_pca)]
    client.insert_rows(table, row_to_insert)

    sentence_json = {'sentence_to_encode': sentence_to_encode,
                     'sentence_embedding': sentence_embedding}
    print(sentence_json)
    producer.send('kafka_1_to_kafka_2', sentence_json)


for msg in consumer:
    encode_and_send(msg)
