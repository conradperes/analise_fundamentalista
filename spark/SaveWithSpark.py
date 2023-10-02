from pyspark.sql import SparkSession
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import date, datetime
import yfinance as yf
import os

class SaveWithSpark:
    def __init__(self, spark_app_name):
        self.spark = SparkSession.builder \
            .appName(spark_app_name) \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "2g") \
            .getOrCreate()

    def read_csv_to_spark_df(self, df):
        pandas_df = df
        return self.spark.createDataFrame(pandas_df)

    @staticmethod
    def prepare_data_to_influxdb(ticker, row):
        date_formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]

        for date_format in date_formats:
            try:
                # Converta o número de ponto flutuante para uma string antes de analisar
                timestamp_str = str(row[0])
                timestamp = datetime.strptime(timestamp_str, date_format)
                break  # Saia do loop se a conversão for bem-sucedida
            except ValueError:
                pass
        else:
            # Se nenhum formato for bem-sucedido, imprima uma mensagem de erro
            print(f"Erro ao converter data para o formato esperado: {row[0]}")
            return None

        data_point = Point(ticker) \
            .time(timestamp) \
            .field("Open", row["Open"]) \
            .field("High", row["High"]) \
            .field("Low", row["Low"]) \
            .field("Close", row["Close"]) \
            .field("Adj Close", row["Adj Close"]) \
            .field("Volume", row["Volume"])

        return data_point



    def get_dataframe(self, ticker, start_period, end_period):
        print("Entrou no dataframe")
        start_period = start_period
        end_period = end_period
        try:
            print("Antes do download no dataframe")
            df = yf.download(ticker, start=start_period, end=end_period)
            print("Depois do download no dataframe")
            return df
        except AttributeError as e:
            print(f"Erro ao obter dados do Yahoo Finance: {e}")
            return None

    def write_to_influxdb(self, influxdb_url, token, org, bucket, rows):
        # Criar um objeto InfluxDBClient aqui para evitar problemas de serialização
        client = InfluxDBClient(url=influxdb_url, token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        def write_row(row):
            # Chamar self.prepare_data_to_influxdb diretamente
            data_point = self.prepare_data_to_influxdb(bucket, row)
            print("antes de escrever")
            write_api.write(bucket=bucket, org=org, record=data_point)
            print("depois de escrever")

        # Iterar sobre as linhas diretamente
        for row in rows:
            write_row(row)

    def save_with_spark(self, influxdb_url, df, token, org, bucket):
        # Não é necessário criar um DataFrame do Spark, pois você já tem um DataFrame do pandas (df)
        local_rows = df.values.tolist()

        # Escreva os dados no InfluxDB usando o driver
        self.write_to_influxdb(influxdb_url, token, org, bucket, local_rows)

        self.close_spark_session()

    def close_spark_session(self):
        self.spark.stop()

# Exemplo de uso
if __name__ == "__main__":
    save_spark = SaveWithSpark("InfluxDBWriter")
    ticker = input("Digite o ticker: ")
    ticker = ticker.upper()
    print(f"Você digitou: {ticker}")
    data_atual = date.today()
    primeiro_dia_do_ano = date(data_atual.year-3, 1, 1)
    df = save_spark.get_dataframe(ticker, primeiro_dia_do_ano, data_atual)
    print(df.head())

    # Substitua o endereço IP a seguir pelo endereço do seu InfluxDB
    influxdb_url = "http://172.17.0.2:8086"

    token = os.environ.get("INFLUXDB_TOKEN")
    org = "cmp"
    bucket = "BTC-USD"

    save_spark.save_with_spark(influxdb_url, df, token, org, bucket)
