import os
import sys
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException
from datetime import date

class StockAnalysis:
    def __init__(self, ticker):
        self.ticker = ticker
        self.client = self.get_influx_client()
        self.bucket = ticker
        self.org = "cmp"

    def get_influx_client(self):
        url = os.environ.get("hostname", "localhost")
        #host = "http://localhost:8086" 
        token = os.environ.get("INFLUXDB_TOKEN")
        #url = f"http://{host}:8086"
        if not token:
            raise ValueError("INFLUXDB_TOKEN is not set in the environment variables.")
        
        print(f"Usando token: {token}")
        
        max_retries = 10  # Aumentando o número de tentativas
        retry_delay = 10
        for attempt in range(max_retries):
            try:
                client = InfluxDBClient(url=url, token=token, org="cmp")
                print("Conexão com InfluxDB realizada com sucesso!")
                return client
            except Exception as e:
                print(f"Tentativa {attempt + 1} falhou: {e}")
                if attempt + 1 == max_retries:
                    raise
                time.sleep(retry_delay)


    def create_bucket_if_not_exists(self):
        buckets_api = self.client.buckets_api()
        buckets = buckets_api.find_buckets().buckets
        bucket_exists = any(b.name == self.bucket for b in buckets)
        if not bucket_exists:
            try:
                buckets_api.create_bucket(bucket_name=self.bucket, org=self.org)
                print(f"Bucket '{self.bucket}' criado com sucesso!")
            except ApiException as e:
                raise RuntimeError(f"Erro ao criar o bucket: {e}")
        else:
            print(f"O bucket '{self.bucket}' já existe.")

    def get_dataframe(self, start_period, end_period):
        try:
            df = yf.download(self.ticker, start=start_period, end=end_period)
            if df.empty:
                raise ValueError(f"No data found for ticker {self.ticker}")
            return df
        except Exception as e:
            raise RuntimeError(f"Erro ao obter dados do Yahoo Finance: {e}")

    def prepare_data_to_influxdb(self, df):
        data_points = []
        for index, row in df.iterrows():
            data_point = Point(self.ticker) \
                .time(index) \
                .field("Open", row["Open"]) \
                .field("High", row["High"]) \
                .field("Low", row["Low"]) \
                .field("Close", row["Close"]) \
                .field("Adj Close", row["Adj Close"]) \
                .field("Volume", row["Volume"])
            data_points.append(data_point)
        return data_points

    def persist_influxdb(self, data_points):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=self.bucket, org=self.org, record=data_points)
        print('Dados persistidos no InfluxDB com sucesso!')

    def generate_graph(self, df, start_period, end_period):
        mc = mpf.make_marketcolors(up='g', down='r')
        s = mpf.make_mpf_style(marketcolors=mc)
        mpf.plot(df, type='candle', style=s, volume=True, title=self.ticker, ylabel='Preço (R$)', ylabel_lower='Volume', figratio=(25, 10), figscale=1.5, mav=(3, 6, 9))
        plt.show()
        print('Gráfico gerado com sucesso!')

    def run(self):
        data_atual = date.today()
        primeiro_dia_do_ano = date(data_atual.year-10, 1, 1)
        self.create_bucket_if_not_exists()
        df = self.get_dataframe(primeiro_dia_do_ano, data_atual)
        data_points = self.prepare_data_to_influxdb(df)
        self.persist_influxdb(data_points)
        self.generate_graph(df, primeiro_dia_do_ano, data_atual)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ticker = sys.argv[1].upper()
    else:
        ticker = os.environ.get('ticker', 'default_value').upper()
    
    if ticker == 'DEFAULT_VALUE':
        print("Por favor, forneça o ticker como argumento ou configure a variável de ambiente 'ticker'.")
    else:
        print(f"Você digitou: {ticker}")
        analysis = StockAnalysis(ticker)
        try:
            analysis.run()
        except Exception as e:
            print(f"Erro: {e}")
