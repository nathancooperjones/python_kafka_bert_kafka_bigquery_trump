from google.cloud import bigquery

schema = [
    bigquery.SchemaField('text', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('embedding', 'FLOAT', mode='REPEATED'),
]

client = bigquery.Client()

table_id = 'nates-projects.trump_tweets.trump_tweets_1201_pca_150_results_table'

table = bigquery.Table(table_id, schema=schema)
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

table_id = 'nates-projects.trump_tweets.trump_tweets_1201_pca_150_query_table'

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)
print(
    'Created table {}.{}.{}'.format(table.project, table.dataset_id, table.table_id)
)
