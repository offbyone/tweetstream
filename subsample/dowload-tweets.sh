#!/usr/bin/env bash
set -e
profile="cdsw"

temp_file=`mktemp`
trap "rm -vf $temp_file" INT QUIT

NEXT_TOKEN=""
next_logs() {

    message_file=$1; shift

    if [[ $NEXT_TOKEN == "" ]]; then
        aws --profile=$profile --region=us-west-2 \
            logs get-log-events \
            --log-group-name tweetstream \
            --log-stream-name tweetstream_json \
            --start-from-head \
            --start-time=1445779713 > $temp_file
    else
        aws --profile=$profile --region=us-west-2 \
            logs get-log-events \
            --log-group-name tweetstream \
            --log-stream-name tweetstream_json \
            --start-from-head \
            --start-time=1445779713 \
            --next-token=$NEXT_TOKEN > $temp_file
    fi

    NEXT_TOKEN=$(jq -r ".nextForwardToken" < $temp_file | tr -d '"')
    jq -c '.events[] | .["message"]' < $temp_file >> $message_file
    messages_left=$(jq '.events | length' < $temp_file)
    if [[ $messages_left == 0 ]]; then
        return 1
    else
        return 0
    fi
}

msg_file=$1; shift
while next_logs $msg_file; do
    echo -ne . >&2
done
