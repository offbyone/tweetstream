FROM debian:jessie
MAINTAINER chris <offline@offby1.net>

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y python3 python3-pip ca-certificates wget openjdk-7-jre
RUN apt-get install -y netcat
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
ADD . /stream
WORKDIR /stream
#CMD ./wait STASH 4444 && echo "foo ---> $STASH_PORT_4444_TCP_ADDR $STASH_PORT_4444_TCP_PORT" | nc $STASH_PORT_4444_TCP_ADDR $STASH_PORT_4444_TCP_PORT
CMD ./wait STASH 4444 && ./application.py | nc $STASH_PORT_4444_TCP_ADDR $STASH_PORT_4444_TCP_PORT
