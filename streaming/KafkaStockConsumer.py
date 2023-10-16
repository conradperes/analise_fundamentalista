import logging
from confluent_kafka import Consumer, KafkaError
from influxdb import InfluxDBClient
from influxdb_client import InfluxDBClient, Point
#import json
import os
import sys
sys.path.append('/root/analise_fundamentalista')
from influx.InfluxDBConnection import InfluxDBConnection
from influx.InfluxDBWriter import InfluxDBWriter
class KafkaStockConsumer:
    def __init__(self, topic, influx_client, measurement, group_id='my_consumer_group'):
        self.topic = topic
        self.influx_client = influx_client
        self.measurement = measurement
        self.group_id = group_id

        # Configuração do consumidor Kafka
        self.consumer_conf = {'bootstrap.servers': 'localhost:9092', 'group.id': self.group_id}

        # Inicializar o consumidor
        self.consumer = Consumer(self.consumer_conf)
        self.consumer.subscribe([self.topic])
        #logging.info("Sobrescreveu a o topico = "+self.topic)

    def influxdb_writer(self, data,  bucket_name,  influx_client, measurement):
        # Transformar os dados para o formato InfluxDB
        points = self.buid_point(data)
        
        logging.info("Ponto a inserir no Influxdb")
        logging.info(points)

        try:
            # Escrever dados no InfluxDB
            self.influx_client.write_to_influxdb(influx_client, bucket_name, measurement=influx_measurement, data_points=points)
            #self.influx_client.write_points(points)
            logging.info("Dados escritos no InfluxDB com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao escrever pontos no InfluxDB: {e}")
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

    def buid_point(self, data, ticker):
        points = []
        data_array = data.split()
        open = float(data_array[2])
        #logging.info("array de info que representa msg= " + data_array)
        #point = {
        #    "measurement": self.measurement,
        #    "index" : data_array[0]+ " " +data_array[1],
        #    "fields": {
        #        "close": valor,
        #        "open": float(data_array[3])
        #    }
        #}
        close = float(data_array[3])
        point = Point(ticker) \
                .time(data_array[0]+ " " +data_array[1]) \
                .field("Close", close) \
                .field("Opens", open) \
        
        points.append(point)
        return points

    def consume_messages(self, influx_writer, bucket_name, influx_measurement, influx_connection, ticker):
        i = 0
        try:
            while True:
                i += 1
                msg = self.consumer.poll(3000)
                logging.info(f"Mensagem {i} sendo consumida = "+str(msg.value().decode('utf-8')))
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logging.error(f"Erro no Kafka: {msg.error()}")
                        break

                # Processar a mensagem do Kafka
                data = str(msg.value().decode('utf-8'))
                #logging.info("Decodificou a mensagem")
                data = self.buid_point(data, ticker)
                logging.info(data)
                influx_writer.write_to_influxdb(influx_connection, bucket_name, measurement=influx_measurement, data_points=data)
                logging.info("Salvou no InfluxDB")

        except KeyboardInterrupt:
            pass
        finally:
            self.close_consumer()

    def close_consumer(self):
        try:
            if self.consumer:
                self.consumer.close()
                logging.info("Consumidor Kafka fechado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao fechar o consumidor Kafka: {e}")

# Configuração de logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    kafka_topic = os.environ.get("ticker")
    influx_measurement = '_measurement'
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "cmp"
    url = "http://localhost:8086"
    influx_connection = InfluxDBConnection(url, token, org)
    connection = influx_connection.connect()
    logging.info("conectou no influxdb")
    influx_connection.create_bucket(kafka_topic)
    influx_writer = InfluxDBWriter(influx_connection)
    kafka_consumer = KafkaStockConsumer(topic=kafka_topic, influx_client=connection, measurement=influx_measurement)
    kafka_consumer.consume_messages(influx_writer, kafka_topic, influx_measurement, connection, kafka_topic)
