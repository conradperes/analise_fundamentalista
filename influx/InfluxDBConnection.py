from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
import os

class InfluxDBConnection:
    def __init__(self, url, token, org):
        self.url = url
        self.org = org
        self.token = token
        self.client = None  # Inicializando o cliente como None

    def connect(self):
        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )

        return self.client

    def close(self):
        if self.client:
            self.client.close()

    def query(self, query):
        result = self.client.query_api().query(org=self.org, query=query)
        return result
    
    def create_bucket(self, name):
        try:
            if not self.client.buckets_api().find_bucket_by_name(name):
                self.client.buckets_api().create_bucket(bucket_name=name, org="cmp")
            else:
                print(f"O bucket '{name}' já existe.")
        except Exception as e:
            print(f"Erro ao criar o bucket: {e}")

    def write_points(self, points, measurement):
        if isinstance(points, Point):
            points = [points]

        write_api = self.client.write_api(write_options=WriteOptions(write_precision=WritePrecision.S))
        write_api.write(bucket=self.org, org=self.org, record=points, data_frame_measurement=measurement)

# Exemplo de Uso:
# token = os.environ.get("INFLUXDB_TOKEN")
# org = "cmp"
# url = "http://localhost:8086"
# connection = InfluxDBConnection(url, token, org)
# connection.connect()

# Exemplo de consulta
# result = connection.query("SELECT * FROM BTC_USD._measurement")
# print(result)

# connection.close()
