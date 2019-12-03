# A Python-Kafka-BERT-Kafka-BigQuery-Trump Project

The greatest authors of our time cannot hold the smallest candles compared to the **GENIUS** prose exemplified on Donald Trump's Twitter account.

![](https://media.npr.org/assets/img/2017/05/31/covfefe-trump_custom-2f50bc17c296cd744346c9b0626712bd7336caea-s800-c85.png)
> "Despite the constant negative press covfefe"
>
> -- *Donald J. Trump (@realDonaldTrump)*
>
> 127k retweets

Although we may try to write something with even a fraction of the elegance, we cannot, which is why I built a tool to analyze anything you enter and find the most similar Donald Trump tweet, and see how well that Tweet did when he composed the masterpiece.

![](https://nathancooperjones.com/wp-content/uploads/2019/12/app-screenshot-1204.png)
![](https://nathancooperjones.com/wp-content/uploads/2019/12/app-screenshot-1203.png)

But this project was built as a final project for a big data technologies course for my final year of graduate school, so it can't be as simple as you might think - we need to unleash some big data tools to get the job done. This project seeks to develop a small use-case exemplifying how a workflow for consuming data streams for data science modeling and sending results to another data stream looks, specifically using Python, Apache Kafka messaging, a BERT deep learning model, and Google BigQuery database tables.

![](https://nathancooperjones.com/wp-content/uploads/2019/12/architecture-diagram-trump-thing.png)

## Installation
```bash
git clone https://github.com/nathancooperjones/python_kafka_bert_kafka_bigquery_trump.git

cd python_kafka_bert_kafka_bigquery_trump/python_kafka_bert_kafka_bigquery_trump
pip install -r requirements.txt

cd 00_environment_prep
```

From here, follow the directions in the `README.md` file, then move on to `01_data_prep` to prepare a dataset and `02_run_the_app` to run the application.

For more information on this project's implementation as well as ideas for future improvements, read the `Final Paper.pdf` file in this repository.

-----

P.S. I think this is the best name for a Github repo that I have ever come up with.
