#!/usr/bin/env python
from TWITTER_API import *
import tweepy
import logging
import pymongo

use_pipeline=True
# use_pipeline=False # use False for to create Mongodb in container 
                     # with python use_twitter_api.py
if use_pipeline:
    DBclient = pymongo.MongoClient(host='mongodb', port=27017) 
else:
    DBclient = pymongo.MongoClient(host='localhost', port=27017)

db=DBclient.Twitter

client= tweepy.Client(bearer_token=BEARER_TOKEN,
                      access_token=API_KEY,
                      access_token_secret=API_KEY_SECRET)

if client:
    logging.critical("\n Authentification OK")
else:
    logging.critical("\n Verify your passwords")



# Defining a query search string
#query = 'war in ukraine lang:en -is:retweet'
query = 'berlin cat lang:en -is:retweet'
#query = 'climate change lang:en -is:retweet'
#query = 'Precht Lanz Welzer lang:de -is:retweet'



paginator = tweepy.Paginator(client.search_recent_tweets,tweet_fields=['id','created_at','text', 'author_id'], query=query).flatten(limit=10)
for tweet in paginator:

    user=client.get_user(id=tweet.author_id, user_fields=['name', 'id', 'created_at'])
    db.Tweets.insert_one({"tweet_id": tweet.id, "author_name": user.data.name, "author_id": user.data.id, "tweet_text": tweet.text, "tweet_date" : tweet.created_at, "query": query})

