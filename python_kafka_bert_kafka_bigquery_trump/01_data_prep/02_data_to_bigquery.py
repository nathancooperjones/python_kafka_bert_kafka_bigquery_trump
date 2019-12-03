from google.cloud import bigquery
from python_kafka_bert_kafka_bigquery_trump.config import (CLEANED_TWEETS_FILENAME,
                                                           DATASET_ID,
                                                           SHORT_TWEETS_TABLE_ID)


# Modified from Google's BigQuery documentation:
# https://github.com/googleapis/google-cloud-python/blob/c7cf8ef445370aff574cc0f83befb46f227e5edc/bigquery/docs/snippets.py

client = bigquery.Client()

dataset_ref = client.dataset(DATASET_ID)
table_ref = dataset_ref.table(SHORT_TWEETS_TABLE_ID)
job_config = bigquery.LoadJobConfig()
job_config.schema = [
    bigquery.SchemaField('source', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('text', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('created_at', 'INTEGER', mode='NULLABLE'),
    bigquery.SchemaField('retweet_count', 'FLOAT', mode='NULLABLE'),
    bigquery.SchemaField('favorite_count', 'FLOAT', mode='NULLABLE'),
    bigquery.SchemaField('id_str', 'INTEGER', mode='NULLABLE'),
    bigquery.SchemaField('text_embedding', 'FLOAT', mode='REPEATED'),
    bigquery.SchemaField('text_embedding_pca_150', 'FLOAT', mode='REPEATED'),
]
job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
job_config.autodetect = True

with open(CLEANED_TWEETS_FILENAME, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

job.result()  # waits for table load to complete.

print("Loaded {} rows into {}:{}.".format(job.output_rows, DATASET_ID, SHORT_TWEETS_TABLE_ID))
