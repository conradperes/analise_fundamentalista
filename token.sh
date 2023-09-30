#!/bin/bash

# Faz uma solicitação para obter o token do InfluxDB
INFLUXDB_TOKEN=$(curl -XPOST -H "Content-Type: application/json" -d '{"username":"conrad","password":"711724Cope"}' http://localhost:8086/api/v2/signin | jq -r .token)

# Configura a variável de ambiente
export INFLUXDB_TOKEN=AG99r6UVBsF6zAc7eMxQ1V8xlxpFQ7ffWnlJVEzWK3GzGAi0Lg6D9Gq9OhkBgptmUXGHfYSNJSggMah2hCl4xg==

# Inicia o Docker Compose
INFLUXDB_TOKEN=AG99r6UVBsF6zAc7eMxQ1V8xlxpFQ7ffWnlJVEzWK3GzGAi0Lg6D9Gq9OhkBgptmUXGHfYSNJSggMah2hCl4xg== docker-compose up -d --build

