import yfinance as yf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType
from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta, date
import os
def get_dataframe(ticker, start_period, end_period):
    print("Entrou no dataframe")
    start_date = datetime.now() - timedelta(days=3650)  # 10 anos atrás
    end_date = datetime.now()

    # Obter os dados do Yahoo Finance
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
        return df
    except AttributeError as e:
        print(f"Erro ao obter dados do Yahoo Finance: {e}")
        return None
def write_to_parquet(df, ticker):
    # Salvar como Parquet
    df.write.mode("overwrite").parquet(f"{ticker}_data.parquet")

def write_to_influxdb(df, ticker, spark):
    influx_client = get_influx_client()

    # Selecione apenas as colunas necessárias
    df = df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

    # Renomeie as colunas para corresponder ao seu esquema no InfluxDB
    df = df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'price', 'Adj Close': 'adj_close', 'Volume': 'volume'})

    # Converta o DataFrame do Pandas para o DataFrame do Spark
    df_spark = spark.createDataFrame(df)
    write_to_parquet(df_spark, ticker)
    # Registre a função como um escritor de dados
    #writeSparkInflux(ticker, df_spark)

def writeSparkInflux(ticker, df_spark):
    df_spark.write.format("influxdb") \
        .option("url", "http://localhost:8086") \
        .option("db", "crypto_prices") \
        .option("measurement", ticker) \
        .option("token", os.environ.get("INFLUXDB_TOKEN")) \
        .mode("append") \
        .save()

def get_influx_client():
    token = ""
    org = "cmp"
    host = "http://localhost"
    url = f"{host}:8086"
    client = InfluxDBClient(url=url, token=token, org=org)
    return client

def main():
    # Configurações do Spark
    spark = SparkSession.builder \
    .appName("InfluxDBExample") \
    .config("spark.jars.packages", "org.influxdb:influxdb-java:2.23") \
    .getOrCreate()

    # Parâmetros do DataFrame
    ticker = "BTC-USD"  # Substitua pelo ticker desejado
    hoje = date.today()
    data_inicial = date(hoje.year-10, 1, 1)
    # Criar DataFrame
    df = get_dataframe(ticker, data_inicial, hoje)

    if df is not None:
        # Converta o campo 'Volume' para float
        df['Volume'] = df['Volume'].astype(float)

        # Execute a função de escrita no InfluxDB
        write_to_influxdb(df, ticker,spark)

    # Fechar a sessão do Spark
    spark.stop()

if __name__ == "__main__":
    main()
