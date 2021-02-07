import flask
from flask import request
import pandas as pd
from datetime import datetime as dt
import pickle
import pandas as pd
import tweepy
import unicodedata

app = flask.Flask(__name__)

tweet_classify = pickle.load(open('finalized_model.sav', 'rb'))


def get_tweets(topic, max_count=100):
    """
    Returns 1000 tweets about a topic as a pandas dataframe.
    change number by using max_count
    """
    import json
    with open("keys/api_keys.json") as f:
        data = json.load(f)

    api_key = data["key"]
    api_secret = data["secret"]
    auth = tweepy.OAuthHandler(api_key, api_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    count = 0
    date = []
    tweets = []
    df = pd.DataFrame(columns=['date', 'tweet'])
    for tweet in tweepy.Cursor(api.search, q=topic, count=1000,
                               lang="en",
                               tweet_mode='extended'
                               ).items():

        if(not tweet.full_text.startswith("RT @")):
            tweets.append(str(unicodedata.normalize(
                'NFKD', tweet.full_text).encode('ascii', 'ignore')))
            date.append(tweet.created_at)
            count += 1

        if(count > max_count):
            break

    return pd.DataFrame(data={'date': date, 'tweet': tweets})


# Should work
def to_lower(text):
    """
    Converts text to lowercase
    """
    return text.lower()

# Should work


def new_get_sentiment(classifier, tweet):
    return classifier.predict([tweet])[0]

# Should work


def labeltoval(label):
    t = {'NEGATIVE': -1, 'POSITIVE': 1}
    return t[label]


def new_sentiment_topic(classifier, topic):
    tweets = get_tweets(topic)
    tweets['tweet'] = tweets.tweet.apply(to_lower)
    val = 0
    count = 0
    for tweet in tweets['tweet']:
        x = labeltoval(new_get_sentiment(classifier, tweet))
        val += x
        count += 1
    val = val/count
    return (topic, val)

# Tried and works
# tweet_classify.predict([year])[0]
# get_tweets(year)


@app.route('/', methods=['GET'])
def home():
    year = str(request.args['year'])
    try:
        return str(new_sentiment_topic(tweet_classify, year))
    except KeyError:
        return f'Invalid'
