import pandas as pd
from sentence_transformers import SentenceTransformer


def clean_trump_tweets(filename):
    """
    Validate images to ensure they can all open and do not have duplicates in the image directory.

    Parameters
    -------------
    filename: string
        filename to JSON file as Trump tweets

    Side Effects
    -------------
    This function writes out a new file, 'trump_tweets_cleaned.json', to disk.

    """
    df = pd.read_json(filename, orient='records')

    # make `created_at` valid dateTimes
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

    # get rid of any retweets, if they exist
    df['is_retweet'] = df['is_retweet'].astype(bool)
    df = df[df['is_retweet'] == False]  # noqa

    # get rid of hyperlinks in `text` and reduce down the `source`
    df = df.copy()
    df['text'] = df['text'].replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)
    df['source'] = df['source'].replace(r'Twitter for ', '', regex=True)

    # Trump likes to Tweet the same things over and over again. Let's get rid of that
    df.drop_duplicates(subset='text', inplace=True)

    # Finally, get those sentence embeddings!
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    df['text_embedding'] = pd.Series(model.encode(df['text'].values))

    # Save as .json file
    df.to_json('trump_tweets_cleaned.json', orient='records', lines=True)
