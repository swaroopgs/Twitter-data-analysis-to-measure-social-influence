from apis.twitterapi import get_tweets, get_retweets, get_user_location
from crud import insert_tweets, insert_retweets, recreate_tables, get_all_tweets, get_all_retweets, insert_location_into_tweets, insert_location_into_retweets, session_scope, insert_sentiment_into_tweets, insert_sentiment_into_retweets
import time
from models import Tweets, Retweets
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_data ():
    # recreate_tables()
    # get tweets
    tweets = get_tweets(100)
    # Insert tweets
    insert_tweets(tweets['statuses'])
    # Go through tweets
    for tweet in tweets['statuses']:
        retweet_count = 0
        if tweet['retweet_count']:
            retweet_count = tweet['retweet_count']
        while retweet_count > 0:
            start_time = time.time()
            # get their retweets
            retweets = get_retweets(tweet["id_str"])
            # insert retweets
            insert_retweets(retweets)
            elapsed = time.time() - start_time
            if elapsed < 10:
                time.sleep(10 - elapsed)
            retweet_count -= 100
    get_data()

def get_location():
    with session_scope() as s:
        tweets = s.query(Tweets).all()
    # tweets = get_all_tweets()
        for tweet in tweets:
            print(tweet.geo)
            if tweet.geo is None:
                location = get_user_location(tweet.user_id)
                insert_location_into_tweets(tweet.id_str, location[0]['location'])
    # adding location for retweets
    with session_scope() as s:
        retweets = s.query(Retweets).all()
        for retweet in retweets:
            if retweet.geo is None:
                location = get_user_location(retweet.user_id)
                insert_location_into_retweets(retweet.id_str, location[0]['location'])

def perform_sentiment_analysis():
    with session_scope() as s:
        tweets = s.query(Tweets).all()
        for tweet in tweets:
            sid = SentimentIntensityAnalyzer()
            scores = sid.polarity_scores(tweet.text)
            sentiment = ""
            if scores.get('compound') > 0.0:
                sentiment = 'pos'
            elif scores.get('compound') < 0.0:
                sentiment = 'neg'
            else:
                sentiment = 'neu'
            insert_sentiment_into_tweets(tweet.id_str, sentiment)
            print("inserted")
            print(sentiment)

    with session_scope() as s:
        retweets = s.query(Retweets).all()
        for retweet in retweets:
            sid = SentimentIntensityAnalyzer()
            scores = sid.polarity_scores(retweet.text)
            sentiment = ""
            if scores.get('compound') > 0.0:
                sentiment = 'pos'
            elif scores.get('compound') < 0.0:
                sentiment = 'neg'
            else:
                sentiment = 'neu'
            insert_sentiment_into_retweets(retweet.id_str, sentiment)
            print("inserted")
            print(sentiment)


if __name__ == '__main__':
    print('Collecting....')
    # get_data()
    # get_location()
    perform_sentiment_analysis()