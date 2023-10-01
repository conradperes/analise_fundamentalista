#!/bin/bash

# Create a custom bridge network
docker network create my_network

# Build the Docker image
docker build -t influxdb_with_python .

# Run the InfluxDB container and connect it to the custom network
docker run -d --name influxdb -p 8086:8086 -v --network my_network  influxdb
#docker run -d --name influxdb_container --network my_network -p 8086:8086 influxdb_with_python -v influxdb_data:/var/lib/influxdb  
#docker run -d --name influxdb -p 8086:8086 -v influxdb_data:/var/lib/influxdb  --network my_network -p 8086:8086 influxdb_with_python
INFLUXDB_TOKEN=$(openssl rand -hex 32)

# Exporta o token como uma variável de ambiente
export INFLUXDB_TOKEN
# Wait for InfluxDB to start
sleep 15

# Run the Python script inside a new container on the same network
docker run -e INFLUXDB_TOKEN=$(INFLUXDB_TOKEN) --network my_network influxdb_with_python python3 /save-crypto.py btc-usd
docker ps
