FROM grafana/grafana:12.3.0

RUN grafana-cli plugins install vertamedia-clickhouse-datasource
#ENV GF_INSTALL_PLUGINS="vertamedia-clickhouse-datasource"

EXPOSE 3000

CMD ["/run.sh"]