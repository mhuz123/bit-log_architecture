FROM docker.elastic.co/logstash/logstash:8.12.0

#USER root
#RUN yum install -y gcc make automake autoconf libtool
#USER logstash

RUN logstash-plugin install logstash-output-clickhouse

COPY pipeline.conf /usr/share/logstash/pipeline/logstash.conf

COPY logstash.yml /usr/share/logstash/config/logstash.yml