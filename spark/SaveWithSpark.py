from pyspark.sql import SparkSession
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException
from datetime import date
import yfinance as yf
import os

def get_influxdb_client(influxdb_url, token, org):
    client = InfluxDBClient(url=influxdb_url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    return client, write_api

def prepare_data_to_influxdb(ticker, row):
    timestamp = row['Date']
    data_point = Point(ticker) \
        .time(timestamp) \
        .field("Open", row["Open"]) \
        .field("High", row["High"]) \
        .field("Low", row["Low"]) \
        .field("Close", row["Close"]) \
        .field("Adj Close", row["Adj Close"]) \
        .field("Volume", row["Volume"])
    return data_point

def write_partition_to_influxdb(partition, influxdb_url, token, org, bucket, ticker):
    client, write_api = get_influxdb_client(influxdb_url, token, org)
    points = []

    for row in partition:
        row_dict = row.asDict()
        point = prepare_data_to_influxdb(ticker, row_dict)
        points.append(point)

    write_api.write(bucket=bucket, org=org, record=points)
    client.close()

class SaveWithSpark:
    def __init__(self, spark_app_name, influxdb_url, token, org, bucket):
        self.spark = SparkSession.builder \
            .appName(spark_app_name) \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "2g") \
            .getOrCreate()
        self.influxdb_url = influxdb_url
        self.token = token
        self.org = org
        self.bucket = bucket

    def read_csv_to_spark_df(self, df):
        pandas_df = df
        return self.spark.createDataFrame(pandas_df)

    def get_dataframe(self, ticker, start_period, end_period):
        print("Entrou no dataframe")
        try:
            print("Antes do download no dataframe")
            df = yf.download(ticker, start=start_period, end=end_period)
            df.reset_index(inplace=True)
            print("Depois do download no dataframe")
            return df
        except AttributeError as e:
            print(f"Erro ao obter dados do Yahoo Finance: {e}")
            return None

    def create_bucket_if_not_exists(self):
        self.client, _ = get_influxdb_client(self.influxdb_url, self.token, self.org)
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

    def save_with_spark(self, spark_df, ticker):
        influxdb_url = self.influxdb_url
        token = self.token
        org = self.org
        bucket = self.bucket
        try:
            spark_df.foreachPartition(lambda partition: write_partition_to_influxdb(partition, influxdb_url, token, org, bucket, ticker))
        finally:
            self.close_spark_session()

    def close_spark_session(self):
        self.spark.stop()

# Exemplo de uso
if __name__ == "__main__":
    influxdb_url = os.getenv("hostname", "http://localhost:8086")
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "cmp"
    ticker = os.environ.get('ticker', 'BTC-USD').upper()
    print(f"Você digitou: {ticker}")
    save_spark = SaveWithSpark("InfluxDBWriter", influxdb_url, token, org, ticker)
    data_atual = date.today()
    primeiro_dia_do_ano = date(data_atual.year-30, 1, 1)
    df = save_spark.get_dataframe(ticker, primeiro_dia_do_ano, data_atual)
    print(df.head())

    save_spark.create_bucket_if_not_exists()
    spark_df = save_spark.read_csv_to_spark_df(df)
    save_spark.save_with_spark(spark_df, ticker)