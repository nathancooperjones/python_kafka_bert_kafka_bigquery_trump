import joblib
import pandas as pd
from python_kafka_bert_kafka_bigquery_trump.config import (BERT_MODEL,
                                                           CLEANED_TWEETS_FILENAME,
                                                           PCA_N_COMPONENTS,
                                                           TWEETS_FILENAME)
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA


"""
Validate images to ensure they can all open and do not have duplicates in the image directory.

Parameters
-------------
filename: string
    filename to JSON file as Trump tweets
pca_n_components: list
    list of integers defining the components of pca to try (default [150])

Side Effects
-------------
This function writes out a new file, 'trump_tweets_cleaned.json', to disk, as well as saves
the PCA transformer to disk, if `pca_n_components` is passed.

"""
df = pd.read_json(TWEETS_FILENAME, orient='records')

# make `created_at` valid dateTimes
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

# get rid of any retweets, if they exist
df['is_retweet'] = df['is_retweet'].astype(bool)
df = df[df['is_retweet'] == False]  # noqa
df.drop(columns=['is_retweet'], inplace=True)

# get rid of hyperlinks in `text` and reduce down the `source`
df = df.copy()
df['text'] = df['text'].replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)
df['source'] = df['source'].replace(r'Twitter for ', '', regex=True)

# Trump likes to Tweet the same things over and over again. Let's get rid of that
df.drop_duplicates(subset='text', inplace=True)

# TODO: add more rigiorous handling for missing values so we don't have to drop as much
df.dropna(axis=0, how='any', inplace=True)

# Finally, get those sentence embeddings!
model = SentenceTransformer(BERT_MODEL)
text_embeddings = model.encode(df['text'].values, show_progress_bar=True)
df['text_embedding'] = text_embeddings

for pca_num in PCA_N_COMPONENTS:
    pca = PCA(n_components=pca_num)
    principal_components = pca.fit_transform(text_embeddings)
    df['text_embedding_pca_' + str(pca_num)] = principal_components.tolist()
    joblib.dump(pca, 'pca_{}.joblib'.format(str(pca_num)))

# Save as .json file
df.to_json(CLEANED_TWEETS_FILENAME, orient='records', lines=True)
