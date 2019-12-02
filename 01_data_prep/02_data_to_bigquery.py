from google.cloud import bigquery


# Modified from Google's BigQuery documentation:
# https://github.com/googleapis/google-cloud-python/blob/c7cf8ef445370aff574cc0f83befb46f227e5edc/bigquery/docs/snippets.py

client = bigquery.Client()
filename = '../trump_tweets_cleaned.json'
dataset_id = 'trump_tweets'
table_id = 'trump_tweets_1201_pca'

dataset_ref = client.dataset(dataset_id)
table_ref = dataset_ref.table(table_id)
job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
job_config.autodetect = True

with open(filename, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

job.result()  # waits for table load to complete.

print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))
