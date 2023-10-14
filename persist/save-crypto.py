#importar bibliotecas
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import plotly.graph_objs as go
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException

import requests
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import sys

#import InfluxDBClient
#from queryinflux import QueryInflux

#gerar grários de candle de análise fundamentalista das ações da bolsa de valores a partir do yahoo finance passando o ticker da ação e o período de análise
def generate_graph_upon_ticker_and_period(ticker, start_period, end_period):
    #definir o ticker e o período de análise
    ticker = ticker
    df = get_dataframe(ticker, start_period, end_period)
    #definir o estilo do gráfico
    mc = mpf.make_marketcolors(up='g',down='r')
    s  = mpf.make_mpf_style(marketcolors=mc)
    #plotar o gráfico
    mpf.plot(df, type='candle', style=s, volume=True, title=ticker, ylabel='Preço (R$)', ylabel_lower='Volume', figratio=(25,10), figscale=1.5, mav=(3,6,9))
    #salvar o gráfico
    #plt.savefig('grafico.png')
    #exibir o gráfico
    plt.grid(True)
    #exibir o gráfico
    plt.show(block=False)
    #exibir mensagem de sucesso
    print('Gráfico gerado com sucesso!')

def get_dataframe(ticker, start_period, end_period):
    print("entrou no dataframe")
    start_period = start_period
    end_period = end_period
    #obter os dados do yahoo finance
    try:
        print("antes do download no dataframe")
        df = yf.download(ticker, start=start_period, end=end_period)
        print("depois do download no dataframe")
        return df
    except AttributeError as e:
        print(f"Erro ao obter dados do Yahoo Finance: {e}")
        return None  # Ou outra ação adequada, como retornar um DataFrame vazio ou levantar outra exceção
    
def get_influx_client():
        token = os.environ.get("INFLUXDB_TOKEN")
        org = "cmp"
        host = "http://172.17.0.2"
        url = f"{host}:8086"
        print(token)
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        print('depois de conectar')
        return client
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

def persist_influxdb(client, bucket, measurement, data_points):
        print('antes de escrever')
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org="cmp", record=data_points)
        print('depois de escrever')


#como verificar se o bucket ja existe e se nao existir criar o bucket no influxdb
def create_bucket_if_not_exists(client, bucket, org):
    buckets_api = client.buckets_api()
    # Listar todos os buckets existentes
    buckets = buckets_api.find_buckets()
    # Verificar se o bucket já existe
    bucket_existe = any(bucket.name == bucket for bucket in buckets)
    # Se o bucket não existe, crie-o
    if not bucket_existe:
        try:
            buckets_api.create_bucket(bucket_name=bucket, org=org)
            print(f"Bucket '{bucket}' criado com sucesso!")
        except ApiException as e:
            print(f"Erro ao criar o bucket: {e}")
    else:
        print(f"O bucket '{bucket}' já existe.")

# chamar a funcao
#instanciar o objeto QueryInflux
#influxObject = QueryInflux()
#obter o cliente do influxdb
#ticker = 'PETR4.SA'
# Solicitar ao usuário que digite algo
#ticker = input("Qual a ação que deseja salvar no influxDB e dps visualizar gráfico: ")
def main():
    ticker = os.environ.get("ticker")
    if len(ticker)>0 :
        #ticker = os.environ.get('ticker', 'default_value')
        ticker = str(ticker).upper()
        # Exibir o que o usuário digitou
        print(f"Você digitou: {ticker}")
        data_atual = date.today()
        primeiro_dia_do_ano = date(data_atual.year-3, 1, 1)
        client = get_influx_client()
        if(not client.buckets_api().find_bucket_by_name(ticker)):
            client.buckets_api().create_bucket(bucket_name=ticker, org="cmp")
        #create_bucket_if_not_exists(ticker, client, "cmp")
        #pegar os dados do yahoo finance
        df = get_dataframe(ticker, primeiro_dia_do_ano, data_atual)
        print(df.head(5))
        #preparar os dados para o influxdb
        data_points = prepare_data_to_influxdb(df, ticker)
        #persistir os dados no influxdb
        persist_influxdb(client, ticker, 'measurement1', data_points)
        generate_graph_upon_ticker_and_period(ticker, primeiro_dia_do_ano, data_atual)
    else:
        print("Meu camarada! Digita essa porra desse ticker ai seu arromado! Como vc espera salvar no Influxdb? Sua besta!!!!!!")
main()     