# ATTRIBUTES
# list of number of components to use for PCA on embeddings
PCA_N_COMPONENTS = [150]
# desired BERT model to load
# from https://github.com/UKPLab/sentence-transformers/blob/master/docs/pretrained-models/nli-models.md
BERT_MODEL = 'bert-base-nli-mean-tokens'

# FILENAMES
# path to unprocessed Trump tweets file on local machine
TWEETS_FILENAME = '/home/ubuntu/trump_tweets.json'
# desired path to processed Trump tweets file on local machine outputted from 01_clean_tweets.py
CLEANED_TWEETS_FILENAME = '/home/ubuntu/trump_tweets_cleaned.json'
# path to saved PCA transformer outputted from 01_clean_tweets.py - will need to be adjusted depending on
# n_components
PCA_FILENAME = '/home/ubuntu/pca_150.joblib'

# BIGQUERY
# full BigQuery table id for Tweets table
TWEETS_TABLE_ID = 'nates-projects.trump_tweets.trump_tweets_1203_pca'
SHORT_TWEETS_TABLE_ID = TWEETS_TABLE_ID.rsplit('.')[-1]
# full BigQuery table id for intermediary results table
RESULTS_TABLE_ID = 'nates-projects.trump_tweets.trump_tweets_1203_pca_150_results_table'
SHORT_RESULTS_TABLE_ID = RESULTS_TABLE_ID.rsplit('.')[-1]
# full BigQuery table id for user query table
QUERY_TABLE_ID = 'nates-projects.trump_tweets.trump_tweets_1203_pca_150_query_table'
# dataset ID in BigQuery
DATASET_ID = TWEETS_TABLE_ID.split('.')[1]
