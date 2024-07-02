docker build -t stock .
docker network create custom-net
docker network connect custom-net influxdb
docker network connect custom-net stock
docker inspect influxdb
docker run --name stock --network custom-net \
  -e INFLUXDB_DB=cmp \
  -e ticker=AMZN \
  -e INFLUXDB_USER=conrad \
  -e INFLUXDB_USER_PASSWORD=711724Cope \
  -e INFLUXDB_USER_READ=conrad \
  -e INFLUXDB_USER_WRITE=conrad \
  -e INFLUXDB_ORG=cmp \
  -e INFLUXDB_TOKEN=ac2HcJIpwxrOjfSUVt8NTGsBPkwHqj-_xEZnbtl5Z8BfqLQaZ7X1B9OAi52NmFZGjJ2b1RbY5iXT0iwtBEfnrA== \
  -e hostname=http://172.19.0.3:8086 \
  stock