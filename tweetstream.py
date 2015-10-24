#!/usr/bin/env python
import sys
import encoding_fix
import tweepy
from twitter_authentication import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

class StreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        print(tweet._json)

    def on_error(self, status_code):
        print( 'Error: ' + repr(status_code))
        if status_code == 420:
            # sleep for a minute to back off.
            import time
            print("Backing off.")
            time.sleep(60 * 2) # sleep for 2 mins.
        elif 400 <= status_code < 500:
            print("Bailing due to {}".format(status_code))
            sys.exit(1)

        return False


while 1:
    try:
        l = StreamListener()
        streamer = tweepy.Stream(auth=auth, listener=l)

        keywords = ['cubs']
        streamer.filter(track = keywords)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print("Error: {}".format(e))
