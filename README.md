Tweet stream aggregator.

Takes in a set of twitter users and search terms, and streams those to
Cloudwatch Logs.

Requirements:

* An AWS account
* An AWS IAM user with the user policy based on the template in
  iam-policy-template.json You'll want to change the ARN of the
  Resource in the `LogWriterStatement2015-10-31` statement.
* A twitter API account
* docker-compose

To start, clone this repository, and copy the two credential template files:

```
cp .tweet_env.template .tweet_env
cp .cw_env.template .cw_env

```

Fill in the template variables using your twitter API and AWS information.

The IAM policy in this does not allow the user that writes the log to
create new CW log groups or log streams, you will have to manually
create those yourself. Right now, that means creating a log group
named `tweetstream` and a log stream in it named
`tweetstream_json`. You can do this in your AWS account's console, or
using the AWS CLI.

If you want to tweak the terms, right now that requires editing
`stream/tweetstream.py`

Run `docker-compose build` in the directory that contains
`docker-compose.yml`

Run `docker-compose up -d` in the same directory

At this point, your streamer should be running; if you check your
cloudwatch logs console, you'll start to see entries. If you want to see what's going on in the streamer itself, you can run `docker-compose logs` to tail the stdout/stderr of the two containers.
