#!/usr/bin/env python3
import os
import sys
import encoding_fix
import tweepy

from twitter_authentication import CONSUMER_KEY, ACCESS_TOKEN

def auth(consumer_secret, access_token_secret):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, consumer_secret)
    auth.set_access_token(ACCESS_TOKEN, access_token_secret)
    return auth

# emit status to stderr because stdout is going to cloudwatch
status = sys.stderr

class StreamListener(tweepy.StreamListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sent = 0

    def on_status(self, tweet):
        print(tweet._json)
        self.sent += 1
        if self.sent % 10 == 1:
            print("Emitted {} tweets total".format(self.sent), file=status)

    def on_error(self, status_code):
        print( 'Error: ' + repr(status_code))
        if status_code == 420:
            # sleep for a minute to back off.
            import time
            print("Backing off.")
            time.sleep(60 * 2) # sleep for 2 mins.
        elif 400 <= status_code < 500:
            print("Bailing due to {}".format(status_code), file=status)
            sys.exit(1)

        return False

DEFAULT_KEYWORDS = [
    'quake',
    'earthquake',
    'magnitude',
    'richter',
    'tsunami',
    'seismic',
]

DEFAULT_USERS = [
    37534994,
    94119095,
    1148387713,
    2417085025,
    20953901,
    16664681,
    12804312
]

def main():
    consumer_secret, access_token_secret = os.environ['CONSUMER_SECRET'], os.environ['ACCESS_TOKEN_SECRET']
    api_auth = auth(consumer_secret, access_token_secret)
    if 'TRACK_KEYWORDS' in os.environ:
        keywords = os.environ["TRACK_KEYWORDS"].split(",")
    else:
        keywords = DEFAULT_KEYWORDS

    if 'TRACK_USERS' in os.environ:
        users = os.environ["TRACK_USERS"].split(",")
    else:
        users = [str(u) for u in DEFAULT_USERS]
    print("Tracking keywords: {}".format(keywords), file=status)
    print("Tracking users: {}".format(users), file=status)
    while 1:
        try:
            l = StreamListener()
            print("Starting to listen using {}:{}".format(l, api_auth), file=status)
            streamer = tweepy.Stream(auth=api_auth, listener=l)
            streamer.filter(track=keywords, follow=users)
        except KeyboardInterrupt:
            print("Exit requested", file=status)
            sys.exit(0)
        except SystemExit:
            raise
        except IOError as e:
            if e.errno == errno.EPIPE:
                # EPIPE error
                raise
            else:
                print("IOError: {}".format(e), file=status)
        except Exception as e:
            print("Error: {}".format(e), file=status)
        print("Looping again", file=status)

if __name__ == "__main__":
    main()
