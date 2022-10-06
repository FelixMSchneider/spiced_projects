import pymongo
from sqlalchemy import create_engine
import re
import logging
import random



import time

time.sleep(10)


MDBclient = pymongo.MongoClient(host='mongodb', port=27017)
db = MDBclient.Twitter

## sentiment analysis of the tweets  (Transform)
def analyse_tweets(tweet):
    """This function takes the text from the tweet and does sentiment analysis."""
    text_from_tweet = str(tweet["tweet_text"])
    sentiment = len(text_from_tweet)
    logging.critical("tweet analysing is done")
    return text_from_tweet, sentiment

## write to postgres (Load)
def load(text, sentiment, PG):
    print(text)
    score = sentiment  
    query = "INSERT INTO tweet_table VALUES (%s, %s);"
    PG.execute(query, (text, score))
    logging.critical("Wrote into postgres!")

PG=create_engine("postgresql://postgres:garlic99@postgresdb:5432/twitter", echo=True)
PG.execute("""CREATE TABLE IF NOT EXISTS tweet_table(
tweet_text VARCHAR(500),
sentiment NUMERIC);""")


tweets = list(db.Tweets.find())

for tweet in tweets:
    current_tweet = tweet
    text_from_tweet, sentiment = analyse_tweets(current_tweet)
    load(text_from_tweet, sentiment, PG)

