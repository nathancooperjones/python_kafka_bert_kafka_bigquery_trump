# Step One: Get and Prep the Data!

There are two methods for getting data:

1. Use the [Trump Twitter Archive](http://www.trumptwitterarchive.com/archive) export tool to download all Trump tweets as JSON. Then use the `clean_trump_tweets` function in `01_clean_tweets.py` to clean the file, which will create a new file called `trump_tweets_cleaned.json`. This may take a while since 1) running every Tweet through the BERT model may take some time, and 2) Trump tweets a lot.

or

2. Set up AWS to clone this public dataset I made and cleaned on 12/01/2019 with
```bash
aws cp s3://recycling-classification/trump_tweets_cleaned.json .
```

Once this is done, configure `02_data_to_bigquery.py` with your own BigQuery table information, then run that file to upload the JSON file to BigQuery.
