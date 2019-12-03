import json
import threading

from google.cloud import bigquery
from kafka import KafkaConsumer
from python_kafka_bert_kafka_bigquery_trump.config import (QUERY_TABLE_ID, RESULTS_TABLE_ID, TWEETS_TABLE_ID)


consumer = KafkaConsumer('kafka_1_to_kafka_2',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

client = bigquery.Client()


# a decorator to make a function run asynchronously
def run_function_async(func):
    def wrapped(arg):
        threading.Thread(target=func, args=(arg,)).start()
    return wrapped


@run_function_async
def find_similar_sentence_and_publish(msg):
    sentence_to_encode = msg.value['sentence_to_encode']

    query = (
        """
        #standardSQL
        SELECT
          c.k1 as input_article_title,
          c.k2 as similar_article_title,
          SUM(vv1*vv2) / (SQRT(SUM(POW(vv1,2))) * SQRT(SUM(POW(vv2,2)))) AS similarity
        FROM
        (
          SELECT
            a.key k1, a.val v1, b.key k2, b.val v2
          FROM
          (
            SELECT text key, embedding val
            FROM `{0}`
            WHERE text = "{1}"
            LIMIT 1
           ) a
          CROSS JOIN
          (
            SELECT text key, text_embedding_pca_150 val
            FROM `{2}`
          ) b
        ) c
        , UNNEST(c.v1) vv1 with offset ind1 JOIN UNNEST(c.v2) vv2 with offset ind2 ON (ind1=ind2)
        GROUP BY c.k1, c.k2
        ORDER BY similarity DESC
        LIMIT 1
        """.format(RESULTS_TABLE_ID, sentence_to_encode, TWEETS_TABLE_ID)
    )
    query_job = client.query(
        query,
        location='US',
    )

    result = list(query_job.result())[0]  # `TypeError: 'RowIterator' object is not an iterator` is hilarious

    print(result)

    similar_trump_tweet = result.get('similar_article_title')
    similarity = result.get('similarity')

    query = (
        """
        INSERT `{0}` (user_text, trump_tweet, favorite_count, retweet_count, created_at, similarity)
        (SELECT "{1}", text, favorite_count, retweet_count, created_at, {2}
         FROM `{3}`
         WHERE text = "{4}")
        """.format(QUERY_TABLE_ID,
                   sentence_to_encode,
                   similarity,
                   TWEETS_TABLE_ID,
                   similar_trump_tweet)
    )
    client.query(
        query,
        location='US',
    )


for msg in consumer:
    find_similar_sentence_and_publish(msg)
