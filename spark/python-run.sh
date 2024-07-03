docker run --name save-spark-image --network custom-net \
  -e INFLUXDB_DB=cmp \
  -e ticker=FJPNX \
  -e INFLUXDB_USER=conrad \
  -e INFLUXDB_USER_PASSWORD=711724Cope \
  -e INFLUXDB_USER_READ=conrad \
  -e INFLUXDB_USER_WRITE=conrad \
  -e INFLUXDB_ORG=cmp \
  -e INFLUXDB_TOKEN=DMpI14RcKKEpcI-iG8tZUa7vi1BYy68IThwSQhNsdBfvqGpd2NndldP538pnaHME0_q1eKks2GKhFMn6KfB6xQ== \
  -e hostname=http://172.18.0.2:8086 \
    save-spark-image