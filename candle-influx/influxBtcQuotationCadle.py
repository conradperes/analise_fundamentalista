from numpy import double
import requests
import plotly.graph_objs as go
from datetime import datetime, timedelta

import influxdb_client
import os

from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "cmp"
url = "https://laughing-waddle-4j6rvj4pwp9c5rq-8086.app.github.dev"
print(token)
bucket="conrad"

# Conecta ao InfluxDB
influx_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
#influxdb_database = 'crypto_prices'  # Nome do banco de dados InfluxDB
influxdb_measurement = 'btc_usd_prices'  # Nome da medição InfluxDB

# Configurações da API CoinDesk
start_date = (datetime.now() - timedelta(days=365 * 4)).date()  # Últimos 2 anos
end_date = datetime.now().date()
api_url = f"https://api.coindesk.com/v1/bpi/historical/close.json?start={start_date}&end={end_date}"

# Obtém os dados da API CoinDesk
response = requests.get(api_url)
data = response.json()
# Função para obter a cotação BTC-USD atual
def get_quotation_btc_usd():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    json_data = response.json()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rate_float = json_data['bpi']['USD']['rate_float']
    
    result = {
        'date_with_seconds': current_time,
        'btc_usd_rate': rate_float
    }
    
    return result
#data =  get_quotation_btc_usd()

# Cria o banco de dados se ele não existir
#if not influx_client.health().status == 'pass':
#    influx_client.create_database(influxdb_database)

# Prepara os dados para o InfluxDB
from dateutil import parser

# Prepara os dados para o InfluxDB
data_points = [
    {
        "measurement": influxdb_measurement,
        "time": timestamp,
        "fields": {
            "price_usd": float(price),  # Converter price para float
        },
    }
    for timestamp, price in data['bpi'].items()
]


print(data_points)
# Salva os dados no InfluxDB
write_api = influx_client.write_api(write_options=SYNCHRONOUS)
write_api.write(bucket=bucket, org="cmp", record=data_points)
#write_api.write(bucket=bucket, record=data_points)

# Cria o gráfico de velas
dates = [datetime.strptime(date, "%Y-%m-%d") for date in data['bpi'].keys()]
candlestick = go.Candlestick(
    x=dates,
    open=[price for price in data['bpi'].values()],
    high=[price for price in data['bpi'].values()],
    low=[price for price in data['bpi'].values()],
    close=[price for price in data['bpi'].values()],
)

# Configura o layout do gráfico
layout = go.Layout(
    title=f'Cotações do BTC-USD nos últimos 2 anos',
    xaxis_title='Data',
    yaxis_title='Preço (USD)',
)

# Cria a figura e plota o gráfico
fig = go.Figure(data=[candlestick], layout=layout)
fig.show()
