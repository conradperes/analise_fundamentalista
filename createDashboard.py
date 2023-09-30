import influxdb
import matplotlib.pyplot as plt
import os
from influxdb_client import InfluxDBClient, Point
import mplfinance as mpf
import pandas as pd
#importar bibliotecas


from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import plotly.graph_objs as go
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException
from datetime import datetime, timedelta, date
import requests
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# Configuração do InfluxDBdef get_influx_client():
def get_influx_client():
        token = os.environ.get("INFLUXDB_TOKEN")
        org = "cmp"
        url = "http://localhost:8086"
        print(token)
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        print('depois de conectar')
        return client
# Processa os dados para criação do gráfico
#data = list(result.get_points())

#timestamps = [entry['_time'] for entry in data]
#values = [entry['_value'] for entry in data]

# Cria um gráfico de barras simples
#plt.figure(figsize=(10, 6))
#plt.bar(timestamps, values, align='center', alpha=0.5)
#plt.xlabel('Timestamp')
#plt.ylabel('Valor')
#plt.title('Dados do InfluxDB')
#plt.xticks(rotation=45)
#plt.tight_layout()

# Exibe o gráfico
#plt.show()
def get_dataframe(ticker, start_period, end_period):
    
    start_period = start_period
    end_period = end_period
    #obter os dados do yahoo finance
    df = yf.download(ticker, start=start_period, end=end_period)
    return df


#prepare data to influxdb
def prepare_data_to_influxdb(df, ticker):
   
   data_points = []
   for index, row in df.iterrows():
    data_point = Point(ticker) \
        .time(index) \
        .field("Open", row["Open"]) \
        .field("High", row["High"]) \
        .field("Low", row["Low"]) \
        .field("Close", row["Close"]) \
        .field("Adj Close", row["Adj Close"]) \
        .field("Volume", row["Volume"])
    
    data_points.append(data_point)
   return data_points

#a partir de um dataframe gerar um dashboard
def generate_dashboard(df, ticker):
    #definir o estilo do gráfico
    mc = mpf.make_marketcolors(up='g',down='r')
    s  = mpf.make_mpf_style(marketcolors=mc)
    #plotar o gráfico
    mpf.plot(df, type='candle', style=s, volume=True, title=ticker, ylabel='Preço (R$)', ylabel_lower='Volume', figratio=(25,10), figscale=1.5, mav=(3,6,9))
    #salvar o gráfico
    #plt.savefig('grafico.png')
    #exibir o gráfico
    plt.show()
    #fechar o gráfico
    plt.close()
    #exibir o gráfico
    plt.show(block=False)
    #exibir mensagem de sucesso
    print('Gráfico gerado com sucesso!')

client = get_influx_client()
query_api = client.query_api()
query = 'from(bucket: "MATIC-USD")\
    |> range(start: -1d)\
    |> filter(fn: (r) => r["_measurement"] == "MATIC-USD")\
    |> filter(fn: (r) => r["_field"] == "Close")\
    |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)\
    |> yield(name: "mean")'
query_result = query_api.query(org="cmp", query=query)
print(query_result)
ticker = 'MATIC-USD'
df = get_dataframe(ticker, '2021-01-01', '2021-07-01')
#df = query_result.to_dataframe()    
generate_dashboard(df,ticker)