from pyspark.sql import SparkSession
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import sys
sys.path.append('/workspaces/analise_fundamentalista')
from util.DataFrameTicker import DataFrameTicker
from influx.InfluxDBConnection import InfluxDBConnection
from datetime import datetime, timedelta, date
class InfluxDBWriter:
    def __init__(self, influx_connection):
        self.influx_connection = influx_connection
        #self.spark = spark_session

    def create_bucket_if_not_exists(self, bucket_name):
        # Verificar se o bucket já existe
        self.influx_connection.create_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' criado com sucesso!")

    def write_to_influxdb(self, client, bucket, measurement, data_points):
        print('antes de escrever')
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org="cmp", record=data_points, data_frame_measurement=measurement)
        print('depois de escrever')

    def write_sparkdf(self):
        print("start spark")
        spark = SparkSession.builder.appName("InfluxDBWriterExample").getOrCreate()
        # Sample data (replace this with your own DataFrame)
        data = [("2023-01-01T00:00:00Z", 1.0), ("2023-01-02T00:00:00Z", 2.0)]
        columns = ["time", "value"]
        df = spark.createDataFrame(data, columns)

        # Configure InfluxDB connection parameters
        influxDB_url = "http://localhost:8086"  # Replace with your InfluxDB URL
        influxDB_database = "MATIC"
        influxDB_username = "conrad"
        influxDB_password = "711724Cope"
        #spark.sparkContext.addPyFile("https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.1.1/spark-sql-kafka-0-10_2.12-3.1.1.jar")
        # Write DataFrame to InfluxDB
        df.write \
            .format("influxdb") \
            .option("url", influxDB_url) \
            .option("db", influxDB_database) \
            .option("user", influxDB_username) \
            .option("password", influxDB_password) \
            .option("measurement", "_measurement").save()#.mode("append")
        spark.stop()

# Exemplo de Uso:

token = os.environ.get("INFLUXDB_TOKEN")
org = "cmp"
url = "http://localhost:8086"
influx_connection = InfluxDBConnection(url, token, org)
influx_connection.connect()
influx_writer = InfluxDBWriter(influx_connection)

# Solicitar ao usuário o nome do bucket
bucket_name  = os.environ.get("ticker")
print(bucket_name)
# Criar o bucket se não existir
influx_connection.create_bucket(bucket_name)

# Exemplo de uso:
ticker_data = DataFrameTicker()
data_atual = date.today()
primeiro_dia_do_ano = date(data_atual.year-10, 1, 1)
df = ticker_data.get_dataframe(bucket_name, primeiro_dia_do_ano, data_atual)
if df is not None:
    influx_measurement = "_measurement"
    data_points = ticker_data.prepare_data_to_influxdb(df, influx_measurement)
    influx_writer.write_to_influxdb(influx_connection.client, bucket_name, measurement=influx_measurement, data_points=data_points)
    #influx_writer.write_sparkdf()

influx_connection.close()






