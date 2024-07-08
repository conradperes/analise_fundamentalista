from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import Point
from influxdb_client.rest import ApiException
import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import date
import sys

class FundamentusAnalysis:
    def __init__(self, ticker):
        self.ticker = ticker
        self.client = self.get_influx_client()
        self.bucket = ticker

    def get_influx_client(self):
        token = os.environ.get("INFLUXDB_TOKEN")
        org = "cmp"
        url = "http://localhost:8086"
        print(token)
        client = InfluxDBClient(url=url, token=token, org=org)
        print('depois de conectar')
        return client
    
    def create_bucket_if_not_exists(self, ticker, client, org):
        bucket = ticker.lower()
        buckets_api = client.buckets_api()
        buckets = buckets_api.find_buckets()
        bucket_exists = any(bucket.name == bucket for bucket in buckets)
        if not bucket_exists:
            try:
                buckets_api.create_bucket(bucket_name=bucket, org=org)
                print(f"Bucket '{bucket}' created successfully!")
            except ApiException as e:
                print(f"Error creating bucket: {e}")
        else:
            print(f"The bucket '{bucket}' already exists.")

        

    def prepare_data_to_influxdb(self, df, ticker):
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

    def persist_influxdb(self, client, bucket, measurement, data_points):
        print('antes de escrever')
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org="cmp", record=data_points)
        print('depois de escrever')

    

    def generate_graph_upon_ticker_and_period(self, ticker, start_period, end_period):
        ticker = ticker
        df = self.get_dataframe(ticker, start_period, end_period)
        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        mpf.plot(df, type='candle', style=s, volume=True, title=ticker, ylabel='Preço (R$)', ylabel_lower='Volume', figratio=(25,10), figscale=1.5, mav=(3,6,9))
        plt.grid(True)
        plt.show(block=False)
        print('Gráfico gerado com sucesso!')

    def get_dataframe(self, ticker, start_period, end_period):
        print("entrou no dataframe")
        start_period = start_period
        end_period = end_period
        try:
            print("antes do download no dataframe")
            df = yf.download(ticker, start=start_period, end=end_period)
            print("depois do download no dataframe")
            return df
        except AttributeError as e:
            print(f"Erro ao obter dados do Yahoo Finance: {e}")
            return None

    def prepare_data_to_influxdb(self, df, ticker):
    
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

    def persist_influxdb(self, client, bucket, measurement, data_points):
            print('antes de escrever')
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=bucket, org="cmp", record=data_points)
            print('depois de escrever')

    def create_bucket_if_not_exists(self):
        try:
            print(f"Ta realmente conectado? '{self.client}' ")
            buckets_api = self.client.buckets_api()
            print(f"Pegou o bucket api? '{buckets_api}' ")
            try:
                buckets = buckets_api.find_bucket_by_name(self.bucket)
                print(buckets)
            except ApiException as e:
                raise RuntimeError(f"Erro ao buscar buckets: {e}")

            if buckets is None:
                try:
                    buckets_api.create_bucket(bucket_name=self.bucket, org="cmp")
                    print(f"Bucket '{self.bucket}' criado com sucesso!")
                except ApiException as e:
                    raise RuntimeError(f"Erro ao criar o bucket: {e}")
            else:
                print(f"O bucket '{self.bucket}' já existe.")
            
        except Exception as e:
            raise RuntimeError(f"Erro ao criar ou buscar o bucket: {e}")

   
        
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        ticker = sys.argv[1].upper()
    else:
        ticker = os.environ.get('ticker', 'default_value').upper()
    print(ticker)
    fundamentalAnalysis = FundamentusAnalysis(ticker)
    
    try:
        if ticker is not None and len(ticker) > 0:
            ticker = str(ticker).upper()
            print(f"Você digitou: {ticker}")
            data_atual = date.today()
            primeiro_dia_do_ano = date(data_atual.year-10, 1, 1)
            client = fundamentalAnalysis.get_influx_client()
            fundamentalAnalysis.create_bucket_if_not_exists() # type: ignore
            df = fundamentalAnalysis.get_dataframe(ticker, primeiro_dia_do_ano, data_atual)
            print(df.head(5))
            data_points = fundamentalAnalysis.prepare_data_to_influxdb(df, ticker)
            fundamentalAnalysis.persist_influxdb(client, ticker, 'measurement1', data_points)
            fundamentalAnalysis.generate_graph_upon_ticker_and_period(ticker, primeiro_dia_do_ano, data_atual)
        else:
            print("Querido usuario, por favor digite o ticker, ou salve em um variavel de ambiente usando export ticker=NOME-TICKER ")   
    except Exception as e:
        print(f"Erro ao executar a análise fundamentalista: {e}")  