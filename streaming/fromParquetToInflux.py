from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType, StringType
from datetime import datetime
import pandas as pd
from influxdb import InfluxDBClient
import os
import sys
sys.path.append('/home/conradperes/projetos/analise_fundamentalista')
from util.DataFrameTicker import DataFrameTicker
from influx.InfluxDBConnection import InfluxDBConnection
from spark.InfluxDBWriter import InfluxDBWriter

def read_parquet_to_spark(parquet_file):
    # Criar uma sessão do Spark
    spark = SparkSession.builder.appName("ParquetToInfluxDB").getOrCreate()

    # Ler o arquivo Parquet para um DataFrame do Spark
    df_spark = spark.read.parquet(parquet_file)
    print(df_spark)

    return df_spark

def convert_spark_to_pandas(df_spark):
    # Converter o DataFrame do Spark para um DataFrame do Pandas
    df_pandas = df_spark.toPandas()
    print(df_pandas.head())
    return df_pandas

def write_to_influxdb(df_pandas, measurement, token, influx_url, influx_org, influx_bucket):
    # Criar um cliente InfluxDB
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "cmp"
    url = "http://localhost:8086"
    influx_connection = InfluxDBConnection(url, token, org)
    influx_connection.connect()
    influx_writer = InfluxDBWriter(influx_connection)

    # Preparar os pontos para InfluxDB
    points = []
    for _, row in df_pandas.iterrows():
        point = {
            "measurement": measurement,
            "time": row["timestamp"],  # Substitua "timestamp" pelo nome da coluna de tempo no seu DataFrame
            "fields": row.drop("timestamp").to_dict()  # Excluir a coluna de tempo para evitar duplicatas
        }
        points.append(point)

    # Escrever pontos no InfluxDB
    influx_writer.write_to_influxdb(influx_connection.client, influx_bucket, measurement=measurement, data_points=points)
    print("escreveu")

def main():
    # Nome do arquivo Parquet (altere conforme necessário)
    parquet_file = "BTC-USD_data.parquet"

    # Parâmetros InfluxDB (altere conforme necessário)
    token = os.environ.get("INFLUXDB_TOKEN")
    influx_url = "http://localhost:8086"
    influx_org = "cmp"
    influx_bucket = "BTC-USD"
    measurement = "crypto_prices"  # Nome mais descritivo

    # Ler o arquivo Parquet com PySpark
    df_spark = read_parquet_to_spark(parquet_file)

    # Converter o DataFrame do Spark para um DataFrame do Pandas
    df_pandas = convert_spark_to_pandas(df_spark)

    # Escrever no InfluxDB
    write_to_influxdb(df_pandas, measurement, token, influx_url, influx_org, influx_bucket)

if __name__ == "__main__":
    main()
