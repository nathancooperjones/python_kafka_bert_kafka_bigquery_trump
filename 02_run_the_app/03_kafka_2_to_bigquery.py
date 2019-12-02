import json

from google.cloud import bigquery
import joblib
from kafka import KafkaConsumer


consumer = KafkaConsumer('kafka_1_to_kafka_2',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

pca = joblib.load('../01_data_prep/pca_150.joblib')

client = bigquery.Client()
dataset_id = 'trump_tweets'
table_id = 'trump_tweets_1201_pca_150_results_table'
table_ref = client.dataset(dataset_id).table(table_id)
table = client.get_table(table_ref)

for msg in consumer:
    sentence_to_encode = msg.value['sentence_to_encode']
    sentence_embedding = msg.value['sentence_embedding']

    sentence_embedding_pca = pca.transform([sentence_embedding])[0]

    rows_to_insert = [(sentence_to_encode, sentence_embedding_pca)]
    client.insert_rows(table, rows_to_insert)

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
            FROM `nates-projects.trump_tweets.trump_tweets_1201_pca_150_results_table`
            WHERE text LIKE "{0}"
            LIMIT 1
           ) a
          CROSS JOIN
          (
            SELECT text key, text_embedding val
            FROM `nates-projects.trump_tweets.trump_tweets_1201`
          ) b
        ) c
        , UNNEST(c.v1) vv1 with offset ind1 JOIN UNNEST(c.v2) vv2 with offset ind2 ON (ind1=ind2)
        GROUP BY c.k1, c.k2
        ORDER BY similarity DESC
        LIMIT 1
        """.format(sentence_to_encode)
    )
    query_job = client.query(
        query,
        location="US",
    )

    result = list(query_job.result())[0]  # `TypeError: 'RowIterator' object is not an iterator` is hilarious
    similar_trump_tweet = result.get('similar_article_title')
    similarity = result.get('similarity')

    print(similar_trump_tweet)

    query = (
        """
        INSERT `nates-projects.trump_tweets.trump_tweets_1201_pca_150_query_table` (user_text, trump_tweet, favorite_count, retweet_count, created_at, similarity)
        (SELECT "{0}", text, favorite_count, retweet_count, created_at, {1}
         FROM `nates-projects.trump_tweets.trump_tweets_1201_pca`
         WHERE text = '{2}')
        """.format(sentence_to_encode, similarity, similar_trump_tweet)  # noqa
    )
    client.query(
        query,
        location="US",
    )
