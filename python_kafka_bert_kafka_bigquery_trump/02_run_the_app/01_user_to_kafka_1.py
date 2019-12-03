from datetime import datetime
import json

from google.cloud import bigquery
from kafka import KafkaProducer
from python_kafka_bert_kafka_bigquery_trump.config import QUERY_TABLE_ID


producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
client = bigquery.Client()

while True:
    sentence = input("Type a sentence (or 'q' to quit): ")
    if sentence.strip() == 'q':
        break
    sentence_json = {'sentence_to_encode': sentence}
    future = producer.send('sentence_to_kafka_1', sentence_json)
    result = future.get(timeout=60)

    print('Working on it...')

    query_results = None
    while not query_results:
        query = (
            """
            SELECT * FROM `{0}`
            WHERE user_text LIKE "{1}"
            LIMIT 1
            """.format(QUERY_TABLE_ID, sentence)
        )
        query_job = client.query(
            query,
            location="US",
        )
        query_results = list(query_job.result())

    query_result = query_results[0]
    entered_text = query_result.get('user_text')
    trump_tweet = query_result.get('trump_tweet')
    favorite_count = int(query_result.get('favorite_count'))
    retweet_count = int(query_result.get('retweet_count'))
    created_at = int(query_result.get('created_at')) / 1000
    created_at_pretty = datetime.fromtimestamp(created_at).strftime('%m/%d/%Y at %H:%M:%S %p')
    similarity = query_result.get('similarity')

    print('''
You entered "{0}".
We ran this through a BERT model with PCA applied to determine the most similar Trump tweet:

"{1}"
    '''.format(entered_text, trump_tweet))

    if retweet_count > 10000:
        print('Wow, that is a VERY popular tweet!')
    elif favorite_count > 10000:
        print('This tweet got some buzz!')
    else:
        print("That wouldn't have been the most popular tweet!")

    print('The original tweet got {} favorites and {} retweets.'.format(favorite_count, retweet_count))
    print('The original tweet was published on {}.'.format(created_at_pretty))
    print('Your text scored a similarity score of {} (the lower, the more similar).'.format(similarity))
    print('\n---------\n')

print('I hope you learned how Trump you are!')
