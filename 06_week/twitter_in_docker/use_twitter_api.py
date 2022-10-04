#!/usr/bin/env python
from TWITTER_API import *
import tweepy
import logging

client= tweepy.Client(bearer_token=BEARER_TOKEN,
                      access_token=API_KEY,
                      access_token_secret=API_KEY_SECRET)


if client:
    logging.critical("\n Authentification OK")
else:
    logging.critical("\n Verify your passwords")


print("test: get user name and id from Elon Musk")

elon = client.get_user(username='elonmusk', user_fields=['name', 'id', 'created_at'])
print(elon.data.name)
print(elon.data.id)
print(str(elon.data.created_at))


print("Now do query fror Climate Change and store it in fetched_tweets.txt")

# Defining a query search string
query = 'climate change lang:en -is:retweet'

paginator = tweepy.Paginator(client.search_recent_tweets,tweet_fields=['id','created_at','text', 'author_id'], query=query).flatten(limit=10)
for tweet in paginator:

    user=client.get_user(id=tweet.author_id, user_fields=['name', 'id', 'created_at'])

    ofile = open('fetched_tweets.txt',mode='a')
    print(f'\n\n\nTWEET with ID {tweet.id} FROM {user.data.name} WITH ID {user.data.id}:\n{tweet.text}\n\n\n',  file=ofile)
    ofile.close()
                                         
