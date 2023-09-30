import requests
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import plotly.graph_objs as go
from datetime import datetime

# Obtém a data de início e fim do mês atual
today = datetime.today()
start_date = today.replace(year=today.year - 5)  # 5 anos atrás a partir de hoje
end_date = today

# Formata as datas no formato esperado pela API CoinDesk (AAAA-MM-DD)
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# URL da API CoinDesk para cotações diárias de Bitcoin USD do mês atual
api_url = f"https://api.coindesk.com/v1/bpi/historical/close.json?start={start_date_str}&end={end_date_str}"

# Faça a solicitação à API CoinDesk
response = requests.get(api_url)
data = response.json()

# Conecte-se ao InfluxDB
token = "Cf15LHUY4Fc9QwfD61zremmmVHhOgzsZtgKwgxIPbPi48hz1gUDkUTg-5ZMpSMF_9yrMdCrv3fMebB_Ow3gb4g=="  # Substitua pelo seu token
org = "cmp"  # Substitua pela sua organização
bucket = "bitcoinmf"  # Substitua pelo seu bucket
url = "http://localhost:8086"

influx_client = InfluxDBClient(url=url, token=token, org=org)

# Prepara os dados para o InfluxDB e escreve no banco de dados
write_api = influx_client.write_api(write_options=SYNCHRONOUS)
data_points = []

for date, price in data["bpi"].items():
    timestamp = datetime.strptime(date, "%Y-%m-%d")
    data_points.append(Point("btc_usd_prices").time(timestamp).field("price_usd", float(price)))

#print(data_points)
write_api.write(bucket=bucket, org=org, record=data_points)

# Cria o gráfico com Plotly
dates = [datetime.strptime(date, "%Y-%m-%d") for date in data["bpi"].keys()]
prices = [float(price) for price in data["bpi"].values()]

trace = go.Scatter(x=dates, y=prices, mode="lines", name="BTC-USD Prices")
layout = go.Layout(
    title="Cotações de BTC-USD do Mês Atual (2023)",
    xaxis_title="Data",
    yaxis_title="Preço (USD)",
)
fig = go.Figure(data=[trace], layout=layout)
fig.show()






