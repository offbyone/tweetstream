import encoding_fix
import datetime
import json
import sys

tweets = open(sys.argv[1], encoding='utf-8')
tweets_by_day = dict()

for line in tweets:
    tweet_as_dictionary = json.loads(line)
    tweet_daytime = datetime.datetime.fromtimestamp(int(tweet_as_dictionary['timestamp_ms']) / 1000)
    tweet_day = tweet_daytime.strftime('%Y-%m-%d')
    if tweet_day not in tweets_by_day:
        tweets_by_day[tweet_day] = 0
    tweets_by_day[tweet_day] += 1
    
print("day,numtweets")
for date in sorted(tweets_by_day.keys()):
    print("{0},{1}".format(date, tweets_by_day[date]))

