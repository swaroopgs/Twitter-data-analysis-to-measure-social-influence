from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from models import Tweets, Retweets
from models import Base

DATABASE_URI = 'postgres+psycopg2://postgres:root@localhost:5432/datascience'

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
conn = engine.connect()


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def recreate_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert_tweets(tweets):
    rows = []
    for tweet in tweets:
        rows.append(Tweets(
            id_str=tweet['id_str'],
            created_at=tweet['created_at'],
            user_id=tweet['user']['id'],
            language=tweet['user']['lang'],
            geo=tweet['geo'],
            text=tweet['text'],
            coordinates=tweet['coordinates']
        ))
    # save tweets in db
    if len(rows):
        with session_scope() as s:
            s.bulk_save_objects(rows)

def insert_retweets(tweets):
    rows = []
    for tweet in tweets:
        if isinstance(tweet, dict):
            rows.append(Retweets(
                origin_id_str=tweet['retweeted_status']['id_str'],
                id_str=tweet['id_str'],
                created_at=tweet['created_at'],
                user_id=tweet['user']['id'],
                language=tweet['user']['lang'],
                geo=tweet['geo'],
                text=tweet['text'],
                coordinates=tweet['coordinates']
            ))
    # save retweets in db
    if len(rows):
        with session_scope() as s:
            s.bulk_save_objects(rows)

def get_all_tweets():
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM tweets")
    # results = cur.fetchall()
    # cur.close()
    # return results
    with session_scope() as s:
        results = s.query(Tweets).all()
        return results

def get_all_retweets():
    with session_scope() as s:
        results = s.query(Retweets).all()
        return results

def insert_location_into_tweets(id_str, location):
    # query = """ UPDATE Tweets
    #             SET geo = %s
    #             WHERE id_str = %s"""
    # cur = conn.cursor()
    # cur.execute(query, (location, id_str))
    # conn.commit()
    # cur.close()

    with session_scope() as s:
        dataToUpdate = {Tweets.geo: location} 
        TweetData = s.query(Tweets).filter(Tweets.id_str==id_str)
        TweetData.update(dataToUpdate)
        s.commit()

def insert_location_into_retweets(id_str, location):

    with session_scope() as s:
        dataToUpdate = {Retweets.geo: location} 
        reTweetData = s.query(Retweets).filter(Retweets.id_str==id_str)
        reTweetData.update(dataToUpdate)
        s.commit()

def insert_sentiment_into_tweets(id_str, sentiment):

    with session_scope() as s:
        dataToUpdate = {Tweets.language: sentiment}
        TweetData = s.query(Tweets).filter(Tweets.id_str==id_str)
        TweetData.update(dataToUpdate)
        s.commit()

def insert_sentiment_into_retweets(id_str, sentiment):

    with session_scope() as s:
        dataToUpdate = {Retweets.language: sentiment}
        reTweetData = s.query(Retweets).filter(Retweets.id_str==id_str)
        reTweetData.update(dataToUpdate)
        s.commit()    
    
            


