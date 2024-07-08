docker run --name save-spark-image --network custom-net \
  -e INFLUXDB_DB=cmp \
  -e ticker=BTC-USD \
  -e INFLUXDB_USER=conrad \
  -e INFLUXDB_USER_PASSWORD=711724Cope \
  -e INFLUXDB_USER_READ=conrad \
  -e INFLUXDB_USER_WRITE=conrad \
  -e INFLUXDB_ORG=cmp \
  -e INFLUXDB_TOKEN=5h4SQ0LxxDq7hBLJrTsa9FT_bHDzeSItc1w5vOEoR6iF-ZBWwAONSbmeVgHiyWlGy7WmWaBj3cSutMLlCxsEpA== \
  -e hostname=http://localhost:8086 \
    save-spark-image