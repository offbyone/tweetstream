FROM logstash:1.5
VOLUME /data-dir

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get -y install rubygems netcat
RUN /opt/logstash/vendor/jruby/bin/jruby -S gem install logstash-core logstash-output-cloudwatchlogs
RUN /opt/logstash/bin/plugin install logstash-output-cloudwatchlogs
ADD logstash.conf /config-dir/logstash.conf
EXPOSE 4444
CMD /opt/logstash/bin/logstash --verbose -f /config-dir/logstash.conf
