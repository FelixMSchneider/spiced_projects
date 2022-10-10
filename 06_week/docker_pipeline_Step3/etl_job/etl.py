import pymongo
from sqlalchemy import create_engine
import re
import logging
import random

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

analyzer = SentimentIntensityAnalyzer()



#use_pipeline=False 
# for single call python etl.py use False
# make sure that mongodb is running in docker container with Twitter database
# ---> e.g. set use_pipeline=False in use_twitter_api.py and run "python use_twitter_api.py" to create Twitter DB with Mongodb outside pipeline

use_pipeline=True

if use_pipeline:
    MDBclient = pymongo.MongoClient(host='mongodb', port=27017)
    usePsql=True
    time.sleep(10)
else:
    MDBclient = pymongo.MongoClient(host='localhost', port=27017)
    usePsql=False

db = MDBclient.Twitter


## sentiment analysis of the tweets  (Transform)

def sentiment_score(text):
    "This function returns a dict of sentiment scores for a given text"
    scores = analyzer.polarity_scores(text)
    return scores

def analyse_tweets(tweet, analyzer):
    """This function takes the text from the tweet and does sentiment analysis."""
    text_from_tweet = str(tweet["tweet_text"])
    sentiment_dict = analyzer.polarity_scores(text_from_tweet)
    sentiment=sentiment_dict["compound"]
    logging.critical("tweet analysing is done")
    return sentiment

## write to postgres (Load)
def load(t_id, a_id, a_name, text, tw_query, score, PG):
    query = "INSERT INTO tweet_table VALUES (%s, %s, %s, %s, %s, %s);"
    PG.execute(query, (int(t_id), int(a_id), str(a_name), str(text), str(tw_query), float(score)))
    logging.critical("Wrote into postgres!")

if usePsql: 
    PG=create_engine("postgresql://postgres:garlic99@postgresdb:5432/twitter", echo=True)
    PG.execute("""CREATE TABLE IF NOT EXISTS tweet_table(
    tweet_id    BIGINT,
    author_id   BIGINT,
    author_name VARCHAR(200),
    tweet_text  VARCHAR(500),
    query       VARCHAR(500),
    sentiment   NUMERIC);""")
    
    
tweets = list(db.Tweets.find())

for tweet in tweets:
    current_tweet = tweet
    sentiment = analyse_tweets(current_tweet, analyzer)

    if usePsql: 
        load(int(tweet["tweet_id"]), int(tweet["author_id"]),str(tweet["author_name"]),str(tweet["tweet_text"]), str(tweet["query"]), float(sentiment), PG)

    else:
        text_from_tweet=current_tweet["tweet_text"]
        print("Tweet:")
        print(text_from_tweet)
        print("score:")
        print(sentiment)
        print("----------------------------------------------------")
        print("XXXX")
        print(" 1)", tweet["tweet_id"], "\n 2)", tweet["author_id"],"\n 3)",tweet["author_name"],"\n 4)",tweet["tweet_text"],"\n 5)", tweet["query"],"\n 6)", sentiment, "\n    XXXX")
        print("----------------------------------------------------")


