import requests
from sqlalchemy import create_engine
import time


time.sleep(5)

webhook_url = "https://hooks.slack.com/services/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" # this is the url of the grumpy cat slack bot Jean-Claude Schulze

use_container=True

if use_container:
    PG=create_engine("postgresql://postgres:garlic99@postgresdb:5432/twitter", echo=True)
else:
    PG=create_engine("postgresql://postgres:garlic99@localhost:5555/twitter", echo=True)

mytweets=PG.execute("SELECT * FROM tweet_table").all()


for tweet in mytweets:
    author_name=tweet[2]
    message=tweet[3]
    data = {'text': author_name + ": " + message}
    requests.post(url=webhook_url, json = data)






