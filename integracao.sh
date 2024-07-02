
docker build -t stock .
docker network create custom-net
docker network connect custom-net influxdb
docker network connect custom-net stock
docker inspect influxdb
docker run --name stock --network custom-net \
  -e INFLUXDB_DB=cmp \
  -e ticker=NVDA \
  -e INFLUXDB_USER=conrad \
  -e INFLUXDB_USER_PASSWORD=711724Cope \
  -e INFLUXDB_USER_READ=conrad \
  -e INFLUXDB_USER_WRITE=conrad \
  -e INFLUXDB_ORG=cmp \
  -e INFLUXDB_TOKEN=y1F6vGWAN2ipu8iVCpSSPucvP6pmgPHs-saH69TuAEMieKEEmcjHfKA-_nrIwvC91SLPEEeJIDC7TW6Y41x8Pw== \
  -e hostname=http://172.18.0.2:8086 \
  stock-analysis