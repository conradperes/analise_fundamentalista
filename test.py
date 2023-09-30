import requests
import pandas as pd
from influxdb import InfluxDBClient
import influxdb_client, os, time
# Configurações do InfluxDB
host = 'localhost'
port = 8086
database = 'bitcoinmf'
username = 'conrad'
password = '711724Cope'

# Configurações da API CoinDesk
api_url = 'https://api.coindesk.com/v1/bpi/historical/close.json'
end_date = pd.Timestamp.now()
start_date = end_date - pd.DateOffset(years=5)

# Parâmetros da solicitação HTTP
params = {
    'start': start_date.strftime('%Y-%m-%d'),
    'end': end_date.strftime('%Y-%m-%d'),
}

# Faça a solicitação à API CoinDesk
response = requests.get(api_url, params=params)
data = response.json()

# Preparar dados para o InfluxDB
btc_prices = data['bpi']
data_points = []

for date, price in btc_prices.items():
    data_points.append({
        "measurement": "btc_usd_prices",
        "time": date,
        "fields": {
            "price_usd": float(price)
        }
    })

# Conectar-se ao InfluxDB
token = os.environ.get("INFLUXDB_TOKEN")
org = "cmp"
url = "http://localhost:8086"
print(token)
client = InfluxDBClient.InfluxDBClient(url=url, token=token, org=org)
#client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)

# Escrever os pontos de dados no InfluxDB
client.write_points(data_points)

print("Dados do BTC inseridos no InfluxDB com sucesso!")
