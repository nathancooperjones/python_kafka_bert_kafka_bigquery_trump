from google.cloud import bigquery
from python_kafka_bert_kafka_bigquery_trump.config import (QUERY_TABLE_ID, RESULTS_TABLE_ID)


schema = [
    bigquery.SchemaField('text', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('embedding', 'FLOAT', mode='REPEATED'),
]

client = bigquery.Client()

table = bigquery.Table(RESULTS_TABLE_ID, schema=schema)
table = client.create_table(table)
print(
    'Created table {}.{}.{}'.format(table.project, table.dataset_id, table.table_id)
)

schema = [
    bigquery.SchemaField('user_text', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('trump_tweet', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('favorite_count', 'FLOAT', mode='NULLABLE'),
    bigquery.SchemaField('retweet_count', 'FLOAT', mode='NULLABLE'),
    bigquery.SchemaField('created_at', 'INTEGER', mode='NULLABLE'),
    bigquery.SchemaField('similarity', 'FLOAT', mode='NULLABLE'),
]

client = bigquery.Client()

table = bigquery.Table(QUERY_TABLE_ID, schema=schema)
table = client.create_table(table)
print(
    'Created table {}.{}.{}'.format(table.project, table.dataset_id, table.table_id)
)
