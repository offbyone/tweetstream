FROM debian:jessie
MAINTAINER chris <offline@offby1.net>

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip python3-setuptools ca-certificates wget openjdk-7-jre netcat strace
ADD . /stream
WORKDIR /stream
RUN python3 setup.py install
CMD ./wait STASH 4444 && ./application.py | nc $STASH_PORT_4444_TCP_ADDR $STASH_PORT_4444_TCP_PORT
#CMD ./application.py
