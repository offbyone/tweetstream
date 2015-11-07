# downsample tweet stream by user.
# allows user-specified salt.
# Usage: python downsample_tweets.py 0.01 salt < full_tweets.json > sample_tweets.json



import sys
import json
import md5

sample_granularity = 1000
sample_percent = float(sys.argv[1]) * sample_granularity
salt = sys.argv[2] if len(sys.argv) > 2 else ''

for line in sys.stdin:
	tweet = json.loads(line) 
	user_id = tweet['user']['id']
	hashed = md5.md5(str(user_id) + salt)
	int_hash = int(hashed.hexdigest(), 16)
	
	# take low order hashes
	if int_hash % sample_granularity < sample_percent:
		print(line),
